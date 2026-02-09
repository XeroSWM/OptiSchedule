# app.py
import streamlit as st
import pandas as pd
from config import CSS_ESTILOS, SLOTS_BASE
from funciones import (
    inicializar_estado, eliminar_item, agregar_ingeniero, agregar_materia, 
    agregar_aula, reparar_datos, abrir_modal_paralelo, cerrar_modal_paralelo, 
    confirmar_paralelo
)
from motor import ejecutar_optimizacion
from reportes import generar_pdf_horario, generar_excel_inteligente 

# 1. Configuración Inicial
st.set_page_config(page_title="OptiSchedule AI", page_icon="✨", layout="wide")
st.markdown(CSS_ESTILOS, unsafe_allow_html=True)
inicializar_estado()

# --- MEMORIA GLOBAL ---
if 'horario_db' not in st.session_state:
    st.session_state['horario_db'] = pd.DataFrame(columns=['Carrera', 'Semestre', 'Día', 'Hora', 'Materia', 'Aula', 'Docente'])

# 2. Sidebar (Minimalista)
with st.sidebar:
    st.title("✨ OptiSchedule")
    st.caption("Sistema de Planificación Inteligente")
    st.write("")
    
    # Filtro Carrera
    if st.session_state['materias']:
        carreras_encontradas = sorted(list(set([str(m.get('carrera', 'Sistemas')) for m in st.session_state['materias']])))
    else:
        carreras_encontradas = ["Sistemas", "Computación", "Diseño Industrial", "Civil"]
        
    carrera_activa = st.selectbox("Selecciona tu carrera", carreras_encontradas)
    
    st.divider()
    menu = st.radio("Navegación", ["📂 Cargar Datos", "👥 Docentes", "📚 Malla", "🏫 Aulas", "🚀 Generar Horario"])
    
    st.divider()
    if st.button("🧹 Limpiar Todo"):
        st.session_state['horario_db'] = pd.DataFrame(columns=['Carrera', 'Semestre', 'Día', 'Hora', 'Materia', 'Aula', 'Docente'])
        st.rerun()

# 3. Lógica de Vistas

if menu == "📂 Cargar Datos":
    st.title("📂 Carga de Información")
    st.markdown("Sube tus archivos Excel para alimentar al modelo de optimización.")
    
    # Contenedor limpio
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.subheader("1. Docentes")
        f = st.file_uploader("Excel Docentes", key="u1")
        if f:
            try:
                df = pd.read_excel(f)
                df.columns = df.columns.str.lower().str.strip()
                reparar_datos()
                lista = []
                for idx, row in df.iterrows():
                    d_list = [x.strip() for x in str(row.get('disponibilidad', '')).split(';') if x.strip()]
                    carreras_ing = row.get('carreras') or row.get('areas') or "Todas"
                    lista.append({"id": int(row.get('id', idx+1)), "nombre": row.get('nombre', 'Sin Nombre'), "carreras": str(carreras_ing), "disponibilidad": d_list})
                st.session_state['ingenieros'] = lista
                st.success("✅ Docentes cargados con éxito")
            except Exception as e: st.error(f"Error: {e}")

    with c2:
        st.subheader("2. Materias")
        f = st.file_uploader("Excel Materias", key="u2")
        if f:
            try:
                df = pd.read_excel(f)
                df.columns = df.columns.str.lower().str.strip()
                materias_limpias = []
                for idx, row in df.iterrows():
                    m = row.to_dict()
                    if 'id' not in m or pd.isna(m['id']): m['id'] = 1000 + idx
                    if 'carrera' not in m or pd.isna(m['carrera']): m['carrera'] = "Sistemas"
                    if 'semestre' not in m or pd.isna(m['semestre']): m['semestre'] = 1
                    materias_limpias.append(m)
                st.session_state['materias'] = materias_limpias
                st.success("✅ Malla cargada con éxito")
                st.rerun()
            except Exception as e: st.error(f"Error: {e}")

    with c3:
        st.subheader("3. Aulas")
        f = st.file_uploader("Excel Aulas", key="u3")
        if f:
            try:
                df = pd.read_excel(f)
                df.columns = df.columns.str.lower().str.strip()
                st.session_state['aulas'] = df.to_dict('records')
                st.success("✅ Aulas cargadas con éxito")
            except Exception as e: st.error(f"Error: {e}")

elif menu == "👥 Docentes":
    st.title(f"Gestión de Docentes")
    st.caption(f"Configurando para: {carrera_activa}")
    
    col_btn, col_search = st.columns([1, 3])
    if col_btn.button("➕ Nuevo Docente"): agregar_ingeniero()
    search_ing = col_search.text_input("Buscar docente...", placeholder="Escribe un nombre...")
    
    lista_ing_filtrada = []
    for ing in st.session_state['ingenieros']:
        areas = str(ing.get('carreras', '')).title()
        if (carrera_activa in areas) or ("Todas" in areas) or ("Básicas" in areas):
            lista_ing_filtrada.append(ing)
    
    for ing in lista_ing_filtrada:
        if search_ing.lower() in ing['nombre'].lower():
            uid = ing['id']
            try: idx_real = st.session_state['ingenieros'].index(ing)
            except: continue

            with st.expander(f"👤 {ing['nombre']}", expanded=False):
                c_a, c_b = st.columns([4, 1])
                st.session_state['ingenieros'][idx_real]['nombre'] = c_a.text_input("Nombre", ing['nombre'], key=f"n{uid}")
                if c_b.button("Eliminar", key=f"del{uid}"): eliminar_item('ingenieros', idx_real)
                
                curr = ing.get('disponibilidad', [])
                if isinstance(curr, str): curr = curr.split(';')
                opts = sorted(list(set(SLOTS_BASE + (curr if isinstance(curr, list) else []))))
                st.session_state['ingenieros'][idx_real]['disponibilidad'] = st.multiselect("Disponibilidad", opts, default=curr, key=f"d{uid}")

elif menu == "📚 Malla":
    st.title(f"Malla Curricular")
    st.caption(f"Materias de: {carrera_activa}")
    
    col_btn, col_search = st.columns([1, 3])
    if col_btn.button("➕ Nueva Materia"): agregar_materia(carrera_activa)
    
    materias_carrera = [m for m in st.session_state['materias'] if str(m.get('carrera')) == carrera_activa]
    semestres_disp = sorted(list(set([int(m.get('semestre', 1)) for m in materias_carrera]))) if materias_carrera else [1]
    
    c_filt, c_srch = st.columns([1, 2])
    filtro_sem = c_filt.selectbox("Filtrar Semestre", ["Todos"] + semestres_disp)
    search_mat = c_srch.text_input("Buscar materia...", "")
    
    # Modal Paralelo
    if st.session_state['modal_paralelo']['activo']:
        id_origen = st.session_state['modal_paralelo']['id_materia_origen']
        materia_origen = next((m for m in st.session_state['materias'] if m['id'] == id_origen), None)
        if materia_origen:
            st.markdown(f"<div class='info-box'>✨ Creando paralelo para: <b>{materia_origen['nombre']}</b></div>", unsafe_allow_html=True)
            docentes_compatibles = [i for i in st.session_state['ingenieros'] 
                                    if carrera_activa in str(i.get('carreras', '')) or "Todas" in str(i.get('carreras', '')) or "Básicas" in str(i.get('carreras', ''))]
            ids_comp = {d['id']: d['nombre'] for d in docentes_compatibles}
            
            sel_doc = st.selectbox("Asignar Docente", list(ids_comp.keys()), format_func=lambda x: ids_comp[x])
            c_ok, c_cancel = st.columns(2)
            if c_ok.button("Crear Paralelo"): confirmar_paralelo(sel_doc)
            if c_cancel.button("Cancelar"): cerrar_modal_paralelo(); st.rerun()
            st.divider()

    ing_map = {i['id']: i['nombre'] for i in st.session_state['ingenieros']}
    
    for m in materias_carrera:
        sem_materia = int(m.get('semestre', 1))
        if (filtro_sem == "Todos" or sem_materia == filtro_sem) and search_mat.lower() in m['nombre'].lower():
            idx_real = st.session_state['materias'].index(m)
            uid = m['id']
            with st.expander(f"📘 {m['nombre']} (Sem: {sem_materia})", expanded=False):
                c1, c2, c3 = st.columns([3, 1, 1])
                st.session_state['materias'][idx_real]['nombre'] = c1.text_input("Nombre", value=m['nombre'], key=f"nm_{uid}")
                if c2.button("Paralelo", key=f"dup_{uid}"): abrir_modal_paralelo(uid); st.rerun()
                if c3.button("Borrar", key=f"del_m_{uid}"): eliminar_item('materias', idx_real)
                
                # --- CAMBIO PRINCIPAL AQUÍ (Agregamos columna Alumnos c8) ---
                c4, c5, c6, c7, c8 = st.columns([1, 1, 2, 1, 1]) 
                
                st.session_state['materias'][idx_real]['semestre'] = c4.number_input("Sem", value=sem_materia, key=f"sem_{uid}")
                st.session_state['materias'][idx_real]['horas'] = c5.number_input("Hrs", value=int(m.get('horas', 4)), key=f"hm_{uid}")
                
                did = m.get('docente_id', 0)
                idx_p = list(ing_map.keys()).index(did) if did in ing_map else 0
                st.session_state['materias'][idx_real]['docente_id'] = c6.selectbox("Prof", list(ing_map.keys()), format_func=lambda x: ing_map[x], index=idx_p, key=f"pm_{uid}")
                
                st.session_state['materias'][idx_real]['req_lab'] = c7.selectbox("Lab?", ["NO", "SI"], index=1 if m.get('req_lab') == "SI" else 0, key=f"lm_{uid}")
                
                # Campo Editable de Alumnos
                st.session_state['materias'][idx_real]['alumnos'] = c8.number_input("Alum", value=int(m.get('alumnos', 35)), step=5, key=f"alum_{uid}")

elif menu == "🏫 Aulas":
    st.title("Infraestructura")
    st.caption("Gestión de aulas y laboratorios compartidos")
    
    col_btn, col_search = st.columns([1, 3])
    if col_btn.button("➕ Nueva Aula"): agregar_aula()
    search_aul = col_search.text_input("Buscar aula...", "")
    
    for i, aula in enumerate(st.session_state['aulas']):
        if search_aul.lower() in aula['nombre'].lower():
            with st.expander(f"🏢 {aula['nombre']}", expanded=False):
                c1, c2 = st.columns([3, 1])
                st.session_state['aulas'][i]['nombre'] = c1.text_input("Nombre", value=aula['nombre'], key=f"na_{i}")
                if c2.button("Borrar", key=f"del_a_{i}"): eliminar_item('aulas', i)
                st.session_state['aulas'][i]['capacidad'] = st.number_input("Capacidad", value=aula['capacidad'], key=f"ca_{i}")
                idx_t = 1 if aula['tipo'] == "LAB" else 0
                st.session_state['aulas'][i]['tipo'] = st.selectbox("Tipo", ["TEORIA", "LAB"], index=idx_t, key=f"ta_{i}")

elif menu == "🚀 Generar Horario":
    st.title(f"Generador de Horarios")
    st.caption(f"Optimizando para: {carrera_activa}")
    
    df_global = st.session_state['horario_db']
    df_actual_carrera = df_global[df_global['Carrera'] == carrera_activa]
    
    # Estado actual
    if not df_actual_carrera.empty:
        st.success(f"✅ Horario generado: {len(df_actual_carrera)} clases.")
    else:
        st.info("ℹ️ Aún no has generado un horario para esta carrera.")

    # Bloqueos
    df_otras = df_global[df_global['Carrera'] != carrera_activa]
    bloqueos_set = set()
    if not df_otras.empty:
        st.markdown(f"<div class='info-box'>🔒 <b>Recursos compartidos:</b> Se respetarán {len(df_otras)} horarios de otras carreras.</div>", unsafe_allow_html=True)
        for _, row in df_otras.iterrows():
            bloqueos_set.add((row['Aula'], row['Día'], row['Hora']))
    
    st.write("")
    col_opt, col_check = st.columns([1, 2])
    modo_flex = col_check.checkbox("Modo Flexible (Permitir cruces leves)", value=False)
    
    if col_opt.button("✨ Optimizar Ahora"):
        with st.spinner("Se está calculando la mejor distribución..."):
            reparar_datos()
            df_nuevo = ejecutar_optimizacion(
                st.session_state['ingenieros'], 
                st.session_state['materias'], 
                st.session_state['aulas'], 
                carrera_activa, 
                slots_ocupados=bloqueos_set,
                ignorar_errores=modo_flex
            )
            
            if df_nuevo is not None:
                df_global_limpio = df_global[df_global['Carrera'] != carrera_activa]
                st.session_state['horario_db'] = pd.concat([df_global_limpio, df_nuevo], ignore_index=True)
                st.balloons()
                st.rerun()
            else:
                st.error("No se pudo encontrar una solución óptima. Intenta el modo flexible.")

    # Resultados Visuales
    if not df_actual_carrera.empty:
        st.divider()
        df_vista = df_actual_carrera.sort_values(by=['Semestre', 'Día', 'Hora'])
        
        tab1, tab2, tab3 = st.tabs(["📊 General", "👨‍🏫 Por Docente", "🎓 Por Semestre"])
        
        with tab1:
            st.dataframe(df_vista, use_container_width=True, hide_index=True)
            
            # --- DESCARGA EXCEL MEJORADA (3 PESTAÑAS) ---
            excel_completo = generar_excel_inteligente(df_vista)
            
            c_d1, c_d2 = st.columns(2)
            c_d1.download_button(
                label="💾 Bajar Excel Completo", 
                data=excel_completo, 
                file_name=f"horario_maestro_{carrera_activa}.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # --- PDF GENERAL (Por Semestre) ---
            pdf = generar_pdf_horario(df_vista, "HORARIO GENERAL", carrera_activa, modo="Semestre")
            c_d2.download_button("📄 Bajar PDF General", pdf, f"horario_{carrera_activa}.pdf", "application/pdf")
            
        with tab2:
            lista_docs = sorted(df_vista['Docente'].unique())
            sel_doc = st.selectbox("Ver Docente:", lista_docs)
            if sel_doc:
                sub_df = df_vista[df_vista['Docente'] == sel_doc]
                st.table(sub_df[['Día', 'Hora', 'Materia', 'Aula']])
                
                # --- PDF DOCENTE UNIFICADO (Sin saltos por semestre) ---
                pdf_sub = generar_pdf_horario(sub_df, f"HORARIO INDIVIDUAL", carrera_activa, modo="Docente")
                st.download_button("Descargar PDF Docente", pdf_sub, f"horario_{sel_doc}.pdf", "application/pdf")
        
        with tab3:
            df_vista['Semestre'] = pd.to_numeric(df_vista['Semestre'], errors='coerce').fillna(0).astype(int)
            lista_sems = sorted(df_vista['Semestre'].unique())
            sel_sem = st.selectbox("Ver Semestre:", lista_sems)
            if sel_sem:
                sub_df = df_vista[df_vista['Semestre'] == sel_sem]
                st.table(sub_df[['Día', 'Hora', 'Materia', 'Aula', 'Docente']])
                
                # --- PDF SEMESTRAL ---
                pdf_sub = generar_pdf_horario(sub_df, f"SEMESTRE {sel_sem}", carrera_activa, modo="Semestre")
                st.download_button("Descargar PDF Semestre", pdf_sub, f"horario_sem_{sel_sem}.pdf", "application/pdf")