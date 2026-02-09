# config.py

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS = ["07:00-09:00", "09:00-11:00", "11:00-13:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]
SLOTS_BASE = [f"{d} {h}" for d in DIAS for h in HORAS]

# --- ESTILO GEMINI DARK MODE (CORREGIDO: LETRAS SANAS + COLORES VIBRANTES) ---
CSS_ESTILOS = """
<style>
    /* Usamos la fuente que ya vimos que funciona bien */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&display=swap');

    /* =========================================
       1. FONDO OSCURO (GEMINI BACKGROUND)
       ========================================= */
    [data-testid="stAppViewContainer"] {
        background-color: #131314 !important; /* Fondo principal casi negro */
        color: #e3e3e3 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #444746;
    }

    /* =========================================
       2. TIPOGRAFÍA
       ========================================= */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        font-family: 'Outfit', sans-serif !important;
        color: #e3e3e3 !important; /* Blanco suave */
    }
    
    /* Título con degradado */
    h1 {
        background: linear-gradient(90deg, #8ab4f8, #c58af9); 
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    /* PROTECCIÓN DE ICONOS: Esto evita que se "dañen" las flechas/iconos */
    i, .material-icons, [data-testid="stSidebarNavItems"] span, [data-testid="stExpanderToggleIcon"] {
        font-family: inherit !important;
    }

    /* =========================================
       3. INPUTS Y SELECTORES (CONTRASTE MEJORADO)
       ========================================= */
    
    /* Cajas de texto y selectores (Estado normal) */
    .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {
        background-color: #1e1f20 !important; /* Fondo gris oscuro */
        color: #ffffff !important; /* Texto blanco brillante (Más legible) */
        border: 1px solid #444746 !important;
        border-radius: 8px !important;
    }
    
    /* Al escribir o seleccionar */
    .stTextInput input:focus, div[data-baseweb="select"] > div:focus-within {
        border-color: #8ab4f8 !important; /* Azul Google */
        box-shadow: 0 0 0 1px #8ab4f8 !important;
    }

    /* --- MENÚ DESPLEGABLE (CORRECCIÓN DE "COLOR OSCURO") --- */
    
    /* Fondo del menú desplegable */
    ul[data-baseweb="menu"] {
        background-color: #2d2e30 !important;
        border: 1px solid #444746 !important;
    }
    
    /* Opciones NO seleccionadas */
    li[data-baseweb="option"] {
        color: #e3e3e3 !important;
        background-color: transparent !important;
    }
    
    /* Opciones AL PASAR EL MOUSE o SELECCIONADAS */
    /* Aquí cambiamos el color oscuro por un gris azulado claro para que se lea */
    li[data-baseweb="option"]:hover, li[aria-selected="true"] {
        background-color: #4a4d50 !important; /* Gris más claro visible */
        color: #8ab4f8 !important; /* Azul neón */
        font-weight: 600 !important;
    }
    
    /* Texto de la opción ya elegida en la caja */
    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    /* Etiquetas de los inputs */
    .stTextInput label, .stSelectbox label, .stNumberInput label {
        color: #a8c7fa !important; /* Azul claro */
    }

    /* =========================================
       4. TARJETAS (EXPANDERS)
       ========================================= */
    .streamlit-expanderHeader {
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        border-radius: 12px !important;
        color: #e3e3e3 !important;
    }
    .streamlit-expanderHeader svg {
        fill: #e3e3e3 !important;
    }
    [data-testid="stExpanderDetails"] {
        background-color: #131314 !important;
        border: 1px solid #444746;
        border-top: none;
        border-radius: 0 0 12px 12px;
    }

    /* =========================================
       5. BOTONES (MÁS VISIBLES Y VIBRANTES)
       ========================================= */
    .stButton > button {
        /* Degradado Azul a Violeta Vibrante */
        background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
        color: #ffffff !important; /* BLANCO PURO */
        border: none !important;
        border-radius: 24px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 700 !important; /* Negrita */
        font-size: 16px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
        box-shadow: 0 6px 12px rgba(139, 92, 246, 0.4) !important; /* Resplandor violeta */
        transform: translateY(-2px);
    }

    /* =========================================
       6. EXTRAS
       ========================================= */
    /* Carga de archivos */
    [data-testid="stFileUploader"] {
        background-color: #1e1f20 !important;
        border: 1px dashed #444746 !important;
        border-radius: 12px;
    }
    [data-testid="stFileUploader"] section > button {
        background-color: #3b82f6 !important; /* Azul botón browse */
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Alertas */
    .stAlert {
        background-color: #1e1f20 !important;
        color: #e3e3e3 !important;
        border: 1px solid #444746 !important;
    }
    
    /* Ocultar barra superior nativa */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
</style>
"""