# funciones.py
import streamlit as st
from config import SLOTS_BASE

def inicializar_estado():
    if 'ingenieros' not in st.session_state: st.session_state['ingenieros'] = []
    if 'materias' not in st.session_state: st.session_state['materias'] = []
    if 'aulas' not in st.session_state: st.session_state['aulas'] = []
    if 'modal_paralelo' not in st.session_state: st.session_state['modal_paralelo'] = {"activo": False, "id_materia_origen": None}

def eliminar_item(list_key, idx):
    del st.session_state[list_key][idx]
    st.rerun()

def agregar_ingeniero():
    nid = len(st.session_state['ingenieros']) + 100
    # Por defecto se agrega como "Básicas" (o Todas) para ser visible
    st.session_state['ingenieros'].append({
        "id": nid, 
        "nombre": "Nuevo Ing.", 
        "carreras": "Básicas", # Campo nuevo
        "disponibilidad": []
    })

def agregar_materia(carrera_actual):
    nid = len(st.session_state['materias']) + 100
    st.session_state['materias'].append({
        "id": nid, 
        "nombre": "Nueva Materia", 
        "horas": 4, 
        "alumnos": 30, 
        "req_lab": "NO", 
        "docente_id": 0, 
        "semestre": 1,
        "carrera": carrera_actual # Asignamos la carrera seleccionada automáticamente
    })

def agregar_aula():
    nid = len(st.session_state['aulas']) + 100
    st.session_state['aulas'].append({"id": nid, "nombre": "Nueva Aula", "capacidad": 40, "tipo": "TEORIA"})

def reparar_datos():
    """Asegura que existan los campos 'carrera' y 'semestre' en los datos cargados."""
    if not st.session_state['ingenieros']: return
    
    ids_ings = [i['id'] for i in st.session_state['ingenieros']]
    def_ing = ids_ings[0] if ids_ings else 0
    
    # Reparar Ingenieros
    for ing in st.session_state['ingenieros']:
        if 'carreras' not in ing: ing['carreras'] = "Todas" # Default si no tiene área
        
    # Reparar Materias
    for m in st.session_state['materias']:
        if 'carrera' not in m: m['carrera'] = "Sistemas" # Default legacy
        if 'semestre' not in m: m['semestre'] = 1
        if 'docente_id' not in m or m['docente_id'] not in ids_ings: m['docente_id'] = def_ing

# --- PARALELOS ---
def abrir_modal_paralelo(materia_id):
    st.session_state['modal_paralelo'] = {"activo": True, "id_materia_origen": materia_id}

def cerrar_modal_paralelo():
    st.session_state['modal_paralelo'] = {"activo": False, "id_materia_origen": None}

def confirmar_paralelo(docente_id_nuevo):
    id_origen = st.session_state['modal_paralelo']['id_materia_origen']
    # Buscar índice real por ID
    idx_origen = next((i for i, m in enumerate(st.session_state['materias']) if m['id'] == id_origen), -1)
    
    if idx_origen != -1:
        original = st.session_state['materias'][idx_origen]
        nueva = original.copy()
        
        nombre_base = original['nombre'].split(' (GR')[0]
        # Contar paralelos existentes en ESA carrera
        count = sum(1 for m in st.session_state['materias'] 
                    if nombre_base in m['nombre'] and m.get('carrera') == original.get('carrera'))
        num_grupo = count + 1
        
        nuevo_id = max([m['id'] for m in st.session_state['materias']]) + 1000
        nueva['id'] = nuevo_id
        nueva['nombre'] = f"{nombre_base} (GR{num_grupo})"
        nueva['docente_id'] = docente_id_nuevo
        
        st.session_state['materias'].insert(idx_origen + 1, nueva)
        st.toast(f"✅ Paralelo creado: {nueva['nombre']}", icon="🎉")
        cerrar_modal_paralelo()
        st.rerun()