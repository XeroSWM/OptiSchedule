# motor.py
import pulp
import pandas as pd
import math
import streamlit as st
from config import DIAS

def ejecutar_optimizacion(ingenieros, materias, aulas, carrera_target, slots_ocupados=set(), ignorar_errores=False):
    """
    Motor de optimización con las 6 REGLAS DE ORO implementadas.
    """
    
    # 1. FILTRAR MATERIAS
    materias_filtradas = [m for m in materias if m.get('carrera') == carrera_target]
    
    if not materias_filtradas:
        st.error(f"⚠️ No se encontraron materias para: {carrera_target}")
        return None

    prob = pulp.LpProblem("Horario_Facultad", pulp.LpMinimize)
    vars_index = []
    
    # 2. MAPEO DE DISPONIBILIDAD
    disp_map = {ing['id']: [] for ing in ingenieros}
    all_active_slots = set()
    
    for ing in ingenieros:
        d_list = ing.get('disponibilidad', [])
        if isinstance(d_list, str): d_list = d_list.split(';')
        for s in d_list:
            partes = s.strip().split(' ')
            if len(partes) >= 2:
                d, h = partes[0], partes[1]
                if d in DIAS:
                    disp_map[ing['id']].append((d, h))
                    all_active_slots.add((d, h))

    # 3. GENERACIÓN DE VARIABLES (Aquí se aplican R5 y R6 como FILTROS)
    errores = []
    ids_validos = {i['id'] for i in ingenieros}
    
    for m in materias_filtradas:
        # [R5] COMPETENCIA DOCENTE (Validación)
        # El solver confía en que el ID asignado en 'materias.xlsx' es el especialista correcto.
        # Si el ID no existe en la base de ingenieros, lanzamos error.
        if m['docente_id'] not in ids_validos:
            errores.append(f"❌ [R5] Error Docente: La materia **{m['nombre']}** tiene asignado un ID ({m['docente_id']}) que no existe.")
            continue
        
        franjas = disp_map.get(m['docente_id'], [])
        posibles = 0
        
        for a in aulas:
            # Filtro de Capacidad
            es_virtual = "VIRTUAL" in a['nombre'].upper()
            cap_ok = a['capacidad'] >= m.get('alumnos', 0) or es_virtual
            
            # [R6] INFRAESTRUCTURA ADECUADA (Filtro Lógico)
            # En lugar de una ecuación matemática, usamos lógica:
            # Si la materia pide LAB y el aula es TEORÍA, NO creamos la opción.
            tipo_ok = False
            req_lab = m.get('req_lab', 'NO')
            tipo_aula = a.get('tipo', 'TEORIA')

            if req_lab == "SI":
                if tipo_aula == "LAB": tipo_ok = True
            else:
                if tipo_aula == "TEORIA" or es_virtual: tipo_ok = True
            
            # Modo Flexible (Ignora R6 si el usuario lo pide)
            if ignorar_errores: 
                cap_ok, tipo_ok = True, True
                
            if cap_ok and tipo_ok:
                for f in franjas:
                    dia, hora = f[0], f[1]
                    
                    # Filtro de Ocupación Externa (Carreras previas)
                    if (a['nombre'], dia, hora) in slots_ocupados:
                        continue

                    # Si pasa todos los filtros (R5, R6, Capacidad), creamos la variable
                    vars_index.append((m['id'], a['id'], dia, hora))
                    posibles += 1
        
        if posibles == 0:
            errores.append(f"⛔ Materia **{m['nombre']}**: Sin opciones viables. (Fallo en R6 o disponibilidad docente).")

    if errores and not ignorar_errores:
        st.markdown("<div class='error-box'><b>Conflictos detectados:</b><br>" + "<br>".join(errores) + "</div>", unsafe_allow_html=True)
        return None

    # 4. VARIABLES BINARIAS
    x = pulp.LpVariable.dicts("x", vars_index, cat='Binary')
    
    # ==========================================
    # RESTRICCIONES MATEMÁTICAS (R1 - R4)
    # ==========================================

    # [R1] CUMPLIMIENTO ACADÉMICO
    # Cada materia debe impartirse las horas necesarias (ni más, ni menos).
    for m in materias_filtradas:
        bloques = math.ceil(m.get('horas', 0) / 2)
        valid = [k for k in vars_index if k[0] == m['id']]
        if valid: 
            prob += pulp.lpSum([x[k] for k in valid]) == bloques

    # [R2] UNICIDAD DE ESPACIO
    # Un aula no puede tener 2 clases a la vez.
    for a in aulas:
        if "VIRTUAL" in a['nombre'].upper(): continue
        for d, h in all_active_slots:
            valid = [k for k in vars_index if k[1] == a['id'] and k[2] == d and k[3] == h]
            if valid: 
                prob += pulp.lpSum([x[k] for k in valid]) <= 1

    # [R3] UBICUIDAD DOCENTE
    # Un profesor no puede dar 2 clases a la vez.
    doc_mat_map = {}
    for m in materias_filtradas:
        if m['docente_id'] not in doc_mat_map: doc_mat_map[m['docente_id']] = []
        doc_mat_map[m['docente_id']].append(m['id'])
        
    for did, mats in doc_mat_map.items():
        for d, h in all_active_slots:
            valid = [k for k in vars_index if k[0] in mats and k[2] == d and k[3] == h]
            if valid: 
                prob += pulp.lpSum([x[k] for k in valid]) <= 1

    # [R4] NO CLONACIÓN DE ESTUDIANTES (La Corrección Crítica)
    # Un semestre no puede tener 2 materias a la misma hora.
    semestres_unicos = set(m['semestre'] for m in materias_filtradas)
    
    for sem in semestres_unicos:
        ids_materias_semestre = [m['id'] for m in materias_filtradas if m['semestre'] == sem]
        
        for d, h in all_active_slots:
            # Sumamos todas las clases posibles para este semestre en este horario
            valid = [k for k in vars_index if k[0] in ids_materias_semestre and k[2] == d and k[3] == h]
            if valid:
                # La suma debe ser <= 1 (O tienen 1 clase, o tienen libre)
                prob += pulp.lpSum([x[k] for k in valid]) <= 1

    # ==========================================
    
    # 5. RESOLVER
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    if pulp.LpStatus[prob.status] == 'Optimal':
        res = []
        for k in vars_index:
            if pulp.value(x[k]) == 1:
                m_obj = next((m for m in materias_filtradas if m['id'] == k[0]), {})
                a_obj = next((a for a in aulas if a['id'] == k[1]), {})
                ing_obj = next((i for i in ingenieros if i['id'] == m_obj.get('docente_id')), {})
                
                res.append({
                    "Carrera": m_obj.get('carrera', carrera_target),
                    "Semestre": m_obj.get('semestre', 1),
                    "Día": k[2],
                    "Hora": k[3],
                    "Materia": m_obj.get('nombre', 'Unknown'),
                    "Aula": a_obj.get('nombre', 'Unknown'),
                    "Docente": ing_obj.get('nombre', 'Sin Asignar')
                })
        
        df = pd.DataFrame(res)
        if not df.empty:
            df['Día'] = pd.Categorical(df['Día'], categories=DIAS, ordered=True)
            df = df.sort_values(by=['Semestre', 'Día', 'Hora'])
        return df
    else:
        st.error("⚠️ Infeasible: No se encontró solución matemática. Revisa las restricciones.")
        return None