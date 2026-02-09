import pandas as pd
import random

# ==============================================================================
# 1. DEFINICIÓN DE MALLAS CURRICULARES COMPLETAS (4 CARRERAS)
# ==============================================================================
materias_raw = []

# --- SISTEMAS DE INFORMACIÓN ---
sistemas = [
    {"semestre": 1, "nombre": "Fundamentos de Matemáticas", "horas": 4, "req_lab": "NO", "target": "Euler"},
    {"semestre": 1, "nombre": "Análisis I", "horas": 4, "req_lab": "NO", "target": "Euler"},
    {"semestre": 1, "nombre": "Programación I", "horas": 4, "req_lab": "SI", "target": "Desarrollo"},
    {"semestre": 1, "nombre": "Fundamentos de Sist. de Información", "horas": 2, "req_lab": "NO", "target": "Desarrollo"},
    {"semestre": 1, "nombre": "Física Aplicada", "horas": 4, "req_lab": "SI", "target": "Newton"},
    {"semestre": 2, "nombre": "Matemáticas Discretas", "horas": 3, "req_lab": "NO", "target": "Discretas"},
    {"semestre": 2, "nombre": "Análisis II", "horas": 4, "req_lab": "NO", "target": "Euler"},
    {"semestre": 2, "nombre": "Álgebra Lineal", "horas": 4, "req_lab": "NO", "target": "Euler"},
    {"semestre": 2, "nombre": "Programación II", "horas": 4, "req_lab": "SI", "target": "Desarrollo"},
    {"semestre": 2, "nombre": "Nuevas Tecnologías e Innovación en SI", "horas": 3, "req_lab": "SI", "target": "Web"},
    {"semestre": 2, "nombre": "Comunicación y Lenguaje", "horas": 2, "req_lab": "NO", "target": "Lenguaje"},
    {"semestre": 3, "nombre": "Probabilidades y Estadística", "horas": 4, "req_lab": "NO", "target": "Gauss"},
    {"semestre": 3, "nombre": "Ecuaciones Diferenciales", "horas": 3, "req_lab": "NO", "target": "Euler"},
    {"semestre": 3, "nombre": "Estructura de Datos", "horas": 4, "req_lab": "SI", "target": "Desarrollo"},
    {"semestre": 3, "nombre": "Arquitectura de Computadores", "horas": 4, "req_lab": "SI", "target": "Sistemas"},
    {"semestre": 3, "nombre": "Interfaces de Usuario", "horas": 3, "req_lab": "SI", "target": "Web"},
    {"semestre": 3, "nombre": "Introducción a la Inv. Científica", "horas": 2, "req_lab": "NO", "target": "Lenguaje"},
    {"semestre": 4, "nombre": "Métodos Numéricos", "horas": 4, "req_lab": "SI", "target": "Euler"},
    {"semestre": 4, "nombre": "Algoritmos", "horas": 2, "req_lab": "SI", "target": "Discretas"},
    {"semestre": 4, "nombre": "Sistemas Operativos I", "horas": 4, "req_lab": "SI", "target": "Sistemas"},
    {"semestre": 4, "nombre": "Infraestructura de TI I", "horas": 5, "req_lab": "SI", "target": "Seguridad"},
    {"semestre": 4, "nombre": "Almacenaje de Datos", "horas": 5, "req_lab": "SI", "target": "Datos"},
    {"semestre": 4, "nombre": "Liderazgo", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 5, "nombre": "Marcos de Desarrollo I", "horas": 4, "req_lab": "SI", "target": "Web"},
    {"semestre": 5, "nombre": "Sistemas Operativos II", "horas": 4, "req_lab": "SI", "target": "Sistemas"},
    {"semestre": 5, "nombre": "Infraestructura de TI II", "horas": 4, "req_lab": "SI", "target": "Seguridad"},
    {"semestre": 5, "nombre": "Gestión de Datos", "horas": 4, "req_lab": "SI", "target": "Datos"},
    {"semestre": 5, "nombre": "Análisis y Diseño de Sistemas", "horas": 4, "req_lab": "NO", "target": "Gestión"},
    {"semestre": 6, "nombre": "Servicio Comunitario", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 6, "nombre": "Contabilidad Financiera", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 6, "nombre": "Marcos de Desarrollo II", "horas": 4, "req_lab": "SI", "target": "Web"},
    {"semestre": 6, "nombre": "Análisis de Datos", "horas": 4, "req_lab": "SI", "target": "Datos"},
    {"semestre": 6, "nombre": "Seguridad y Gestión de Riesgos", "horas": 4, "req_lab": "NO", "target": "Seguridad"},
    {"semestre": 6, "nombre": "Desarrollo de SI", "horas": 4, "req_lab": "SI", "target": "Desarrollo"},
    {"semestre": 7, "nombre": "Servicio Comunitario II", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 7, "nombre": "Fundamentos de Economía", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 7, "nombre": "Programación Web", "horas": 4, "req_lab": "SI", "target": "Web"},
    {"semestre": 7, "nombre": "Inteligencia de Negocios", "horas": 4, "req_lab": "SI", "target": "Inteligencia"},
    {"semestre": 7, "nombre": "Investigación Aplicada", "horas": 2, "req_lab": "NO", "target": "Lenguaje"},
    {"semestre": 7, "nombre": "Arquitectura de Software", "horas": 4, "req_lab": "SI", "target": "Sistemas"},
    {"semestre": 7, "nombre": "Sociedad de la Información", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 8, "nombre": "Prácticas Preprofesionales I", "horas": 2, "req_lab": "NO", "target": "Gestión"},
    {"semestre": 8, "nombre": "Auditoría TI", "horas": 4, "req_lab": "NO", "target": "Seguridad"},
    {"semestre": 8, "nombre": "Programación Distribuida", "horas": 4, "req_lab": "SI", "target": "Desarrollo"},
    {"semestre": 8, "nombre": "Minería de Datos", "horas": 4, "req_lab": "SI", "target": "Datos"},
    {"semestre": 8, "nombre": "Investigación Operativa", "horas": 2, "req_lab": "NO", "target": "Discretas"},
    {"semestre": 8, "nombre": "Control de Calidad Software", "horas": 4, "req_lab": "NO", "target": "Testing"},
    {"semestre": 9, "nombre": "Prácticas Preprofesionales II", "horas": 2, "req_lab": "NO", "target": "Gestión"},
    {"semestre": 9, "nombre": "Titulación I (Proyecto)", "horas": 5, "req_lab": "NO", "target": "Agile"},
    {"semestre": 9, "nombre": "Legislación Informática", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 9, "nombre": "Gestión de Procesos (BPM)", "horas": 4, "req_lab": "SI", "target": "Gestión"},
    {"semestre": 9, "nombre": "Modelos de Inv. Operativa", "horas": 3, "req_lab": "NO", "target": "Discretas"},
    {"semestre": 9, "nombre": "Gestión de Proyectos SI", "horas": 4, "req_lab": "NO", "target": "Agile"},
    {"semestre": 10, "nombre": "Prácticas Preprofesionales III", "horas": 2, "req_lab": "NO", "target": "Gestión"},
    {"semestre": 10, "nombre": "Titulación II (Desarrollo)", "horas": 5, "req_lab": "NO", "target": "Agile"},
    {"semestre": 10, "nombre": "Prog. Dispositivos Móviles", "horas": 3, "req_lab": "SI", "target": "Moviles"},
    {"semestre": 10, "nombre": "Formación de Empresas Tech", "horas": 2, "req_lab": "NO", "target": "Gestión"},
    {"semestre": 10, "nombre": "Sistemas de Info. Empresarial", "horas": 4, "req_lab": "SI", "target": "Gestión"},
    {"semestre": 10, "nombre": "Estrategia y Gestión de SI", "horas": 4, "req_lab": "NO", "target": "Gestión"}
]
for m in sistemas: m['carrera'] = "Sistemas"
materias_raw.extend(sistemas)

# --- COMPUTACIÓN ---
computacion = [
    {"semestre": 1, "nombre": "Análisis I", "horas": 6, "req_lab": "NO", "target": "Euler"},
    {"semestre": 1, "nombre": "Fund. Matemática", "horas": 4, "req_lab": "NO", "target": "Euler"},
    {"semestre": 1, "nombre": "Programación I", "horas": 6, "req_lab": "SI", "target": "Turing"},
    {"semestre": 1, "nombre": "Intro Ciencias Comp.", "horas": 2, "req_lab": "NO", "target": "Hopper"},
    {"semestre": 1, "nombre": "Realidad Nacional", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 2, "nombre": "Análisis II", "horas": 6, "req_lab": "NO", "target": "Euler"},
    {"semestre": 2, "nombre": "Álgebra Lineal I", "horas": 4, "req_lab": "NO", "target": "Euler"},
    {"semestre": 2, "nombre": "Programación II", "horas": 6, "req_lab": "SI", "target": "Turing"},
    {"semestre": 2, "nombre": "Física", "horas": 4, "req_lab": "SI", "target": "Newton"},
    {"semestre": 2, "nombre": "Comunicación Oral", "horas": 2, "req_lab": "NO", "target": "Lenguaje"},
    {"semestre": 3, "nombre": "Análisis III", "horas": 6, "req_lab": "NO", "target": "Euler"},
    {"semestre": 3, "nombre": "Álgebra Lineal II", "horas": 4, "req_lab": "NO", "target": "Euler"},
    {"semestre": 3, "nombre": "Estructura de Datos", "horas": 4, "req_lab": "SI", "target": "Hopper"},
    {"semestre": 3, "nombre": "Física para Comp.", "horas": 4, "req_lab": "SI", "target": "Newton"},
    {"semestre": 3, "nombre": "Probabilidad Básica", "horas": 4, "req_lab": "NO", "target": "Gauss"},
    {"semestre": 4, "nombre": "Ecuaciones Diferenciales", "horas": 4, "req_lab": "NO", "target": "Euler"},
    {"semestre": 4, "nombre": "Análisis Numérico", "horas": 4, "req_lab": "SI", "target": "Turing"},
    {"semestre": 4, "nombre": "Matemática Discreta", "horas": 4, "req_lab": "NO", "target": "Euler"},
    {"semestre": 4, "nombre": "Base de Datos I", "horas": 4, "req_lab": "SI", "target": "Hopper"},
    {"semestre": 4, "nombre": "Arquitectura Software", "horas": 4, "req_lab": "NO", "target": "Linus"},
    {"semestre": 5, "nombre": "Inferencia Estadística", "horas": 4, "req_lab": "NO", "target": "Gauss"},
    {"semestre": 5, "nombre": "Base de Datos II", "horas": 4, "req_lab": "SI", "target": "Hopper"},
    {"semestre": 5, "nombre": "Prog. Avanzada I", "horas": 4, "req_lab": "SI", "target": "Turing"},
    {"semestre": 5, "nombre": "Patrones Diseño", "horas": 4, "req_lab": "SI", "target": "Linus"},
    {"semestre": 5, "nombre": "Arq. Entornos Operativos", "horas": 4, "req_lab": "SI", "target": "Linus"},
    {"semestre": 5, "nombre": "Metodología Investigación", "horas": 2, "req_lab": "NO", "target": "Lenguaje"},
    {"semestre": 6, "nombre": "Optimización y Simulación", "horas": 4, "req_lab": "SI", "target": "Turing"},
    {"semestre": 6, "nombre": "Inteligencia Artificial", "horas": 4, "req_lab": "SI", "target": "Turing"},
    {"semestre": 6, "nombre": "Prog. Avanzada II", "horas": 4, "req_lab": "SI", "target": "Hopper"},
    {"semestre": 6, "nombre": "Redes y Protocolos", "horas": 4, "req_lab": "SI", "target": "Redes"},
    {"semestre": 6, "nombre": "Innovación y Emprend.", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 6, "nombre": "Vinculación I", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 7, "nombre": "Aprendizaje Automático", "horas": 4, "req_lab": "SI", "target": "Turing"},
    {"semestre": 7, "nombre": "Prog. Avanzada III", "horas": 4, "req_lab": "SI", "target": "Hopper"},
    {"semestre": 7, "nombre": "Visualización Gráfica", "horas": 4, "req_lab": "SI", "target": "Linus"},
    {"semestre": 7, "nombre": "Ingeniería Software", "horas": 4, "req_lab": "NO", "target": "Hopper"},
    {"semestre": 7, "nombre": "Investigación Aplicada", "horas": 2, "req_lab": "NO", "target": "Lenguaje"},
    {"semestre": 7, "nombre": "Vinculación II", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 8, "nombre": "Dispositivos Móviles", "horas": 4, "req_lab": "SI", "target": "Hopper"},
    {"semestre": 8, "nombre": "Criptografía", "horas": 4, "req_lab": "NO", "target": "Turing"},
    {"semestre": 8, "nombre": "Programación Web", "horas": 4, "req_lab": "SI", "target": "Hopper"},
    {"semestre": 8, "nombre": "Desarrollo Videojuegos", "horas": 4, "req_lab": "SI", "target": "Linus"},
    {"semestre": 8, "nombre": "Gobierno TIC", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 8, "nombre": "Taller I (Tesis)", "horas": 2, "req_lab": "NO", "target": "Lenguaje"},
    {"semestre": 8, "nombre": "Prácticas I", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 9, "nombre": "Minería de Datos", "horas": 4, "req_lab": "SI", "target": "Turing"},
    {"semestre": 9, "nombre": "Sistemas Colaborativos", "horas": 4, "req_lab": "NO", "target": "Hopper"},
    {"semestre": 9, "nombre": "Prog. Concurrente", "horas": 4, "req_lab": "SI", "target": "Linus"},
    {"semestre": 9, "nombre": "Proyecto Videojuegos", "horas": 4, "req_lab": "SI", "target": "Linus"},
    {"semestre": 9, "nombre": "Taller II (Tesis)", "horas": 2, "req_lab": "NO", "target": "Lenguaje"},
    {"semestre": 9, "nombre": "Prácticas II", "horas": 2, "req_lab": "NO", "target": "Marx"},
    {"semestre": 10, "nombre": "Trabajo Titulación", "horas": 10, "req_lab": "NO", "target": "Lenguaje"},
    {"semestre": 10, "nombre": "Prog. Distribuida", "horas": 4, "req_lab": "SI", "target": "Turing"},
    {"semestre": 10, "nombre": "Computación Cloud", "horas": 4, "req_lab": "SI", "target": "Redes"},
    {"semestre": 10, "nombre": "Taller III (Tesis)", "horas": 2, "req_lab": "NO", "target": "Lenguaje"},
    {"semestre": 10, "nombre": "Prácticas III", "horas": 2, "req_lab": "NO", "target": "Marx"}
]
for m in computacion: m['carrera'] = "Computación"
materias_raw.extend(computacion)

# --- DISEÑO INDUSTRIAL ---
diseno = [
    {"semestre": 1, "nombre": "Realidad Nacional", "horas": 2, "req_lab": "NO", "target": "Bernoulli"},
    {"semestre": 1, "nombre": "Diseño Básico", "horas": 4, "req_lab": "SI", "target": "Da Vinci"},
    {"semestre": 1, "nombre": "Dibujo Artístico", "horas": 4, "req_lab": "SI", "target": "Da Vinci"},
    {"semestre": 1, "nombre": "Análisis Mat. I", "horas": 4, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 1, "nombre": "Física I", "horas": 4, "req_lab": "SI", "target": "Einstein"},
    {"semestre": 1, "nombre": "Química", "horas": 4, "req_lab": "SI", "target": "Lavoisier"},
    {"semestre": 2, "nombre": "Expresión Oral", "horas": 2, "req_lab": "NO", "target": "Cervantes"},
    {"semestre": 2, "nombre": "Métodos Diseño", "horas": 3, "req_lab": "NO", "target": "Bauhaus"},
    {"semestre": 2, "nombre": "Dibujo Técnico", "horas": 4, "req_lab": "SI", "target": "Da Vinci"},
    {"semestre": 2, "nombre": "Taller I: Producto", "horas": 5, "req_lab": "SI", "target": "Bauhaus"},
    {"semestre": 2, "nombre": "Análisis Mat. II", "horas": 4, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 2, "nombre": "Física II", "horas": 4, "req_lab": "SI", "target": "Einstein"},
    {"semestre": 3, "nombre": "Historia Diseño", "horas": 3, "req_lab": "NO", "target": "Cervantes"},
    {"semestre": 3, "nombre": "Presentación Digital", "horas": 4, "req_lab": "SI", "target": "Da Vinci"},
    {"semestre": 3, "nombre": "Álgebra Lineal", "horas": 4, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 3, "nombre": "Ing. Materiales", "horas": 4, "req_lab": "SI", "target": "Materiales"},
    {"semestre": 3, "nombre": "Informática Ind.", "horas": 4, "req_lab": "SI", "target": "CAD"},
    {"semestre": 4, "nombre": "Ergonomía Diseño", "horas": 3, "req_lab": "SI", "target": "Ergonomía"},
    {"semestre": 4, "nombre": "Diseño CAD", "horas": 4, "req_lab": "SI", "target": "CAD"},
    {"semestre": 4, "nombre": "Taller II: Conceptual", "horas": 5, "req_lab": "SI", "target": "Bauhaus"},
    {"semestre": 4, "nombre": "Análisis Numérico", "horas": 4, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 4, "nombre": "Resistencia Materiales", "horas": 4, "req_lab": "NO", "target": "Materiales"},
    {"semestre": 5, "nombre": "Envases y Embalajes", "horas": 4, "req_lab": "SI", "target": "Pack"},
    {"semestre": 5, "nombre": "Diseño Mecánico", "horas": 4, "req_lab": "SI", "target": "Materiales"},
    {"semestre": 5, "nombre": "Simulación Prototipos", "horas": 4, "req_lab": "SI", "target": "Da Vinci"},
    {"semestre": 5, "nombre": "Ecuaciones Dif.", "horas": 4, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 5, "nombre": "Termodinámica", "horas": 4, "req_lab": "NO", "target": "Einstein"},
    {"semestre": 6, "nombre": "Emprendimiento", "horas": 2, "req_lab": "NO", "target": "Bernoulli"},
    {"semestre": 6, "nombre": "Taller III: Productos", "horas": 5, "req_lab": "SI", "target": "Bauhaus"},
    {"semestre": 6, "nombre": "Estadística", "horas": 4, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 6, "nombre": "Ing. Producción", "horas": 4, "req_lab": "NO", "target": "Materiales"},
    {"semestre": 6, "nombre": "Gestión Operaciones", "horas": 3, "req_lab": "NO", "target": "Materiales"},
    {"semestre": 7, "nombre": "Legislación Diseño", "horas": 2, "req_lab": "NO", "target": "Bernoulli"},
    {"semestre": 7, "nombre": "Simulación Numérica", "horas": 4, "req_lab": "SI", "target": "CAD"},
    {"semestre": 7, "nombre": "Procesos Manufactura", "horas": 4, "req_lab": "SI", "target": "Materiales"},
    {"semestre": 7, "nombre": "Calidad Total", "horas": 3, "req_lab": "NO", "target": "Materiales"},
    {"semestre": 7, "nombre": "Diseño Sustentable", "horas": 3, "req_lab": "NO", "target": "Eco"},
    {"semestre": 8, "nombre": "Taller IV: Sustentable", "horas": 5, "req_lab": "SI", "target": "Eco"},
    {"semestre": 8, "nombre": "Optimización Procesos", "horas": 4, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 8, "nombre": "Seguridad Industrial", "horas": 3, "req_lab": "NO", "target": "Materiales"},
    {"semestre": 8, "nombre": "Desarrollo Sostenible", "horas": 2, "req_lab": "NO", "target": "Bernoulli"},
    {"semestre": 8, "nombre": "Ecología Industrial", "horas": 2, "req_lab": "NO", "target": "Bernoulli"},
    {"semestre": 9, "nombre": "Metodología Invest.", "horas": 2, "req_lab": "NO", "target": "Cervantes"},
    {"semestre": 9, "nombre": "Fabricación CAM", "horas": 4, "req_lab": "SI", "target": "Procesos"},
    {"semestre": 9, "nombre": "Gestión Diseño", "horas": 3, "req_lab": "NO", "target": "Rams"},
    {"semestre": 9, "nombre": "Eficiencia Energética", "horas": 3, "req_lab": "NO", "target": "Einstein"},
    {"semestre": 10, "nombre": "Ingeniería Económica", "horas": 3, "req_lab": "NO", "target": "Bernoulli"},
    {"semestre": 10, "nombre": "Taller V: Proyectos", "horas": 6, "req_lab": "SI", "target": "Zaha"}
]
for m in diseno: m['carrera'] = "Diseño Industrial"
materias_raw.extend(diseno)

# --- CIVIL ---
civil = [
    {"semestre": 1, "nombre": "Cálculo Diferencial", "horas": 6, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 1, "nombre": "Dibujo CAD", "horas": 3, "req_lab": "SI", "target": "Construcción"},
    {"semestre": 1, "nombre": "Programación 1", "horas": 3, "req_lab": "SI", "target": "Sismología"},
    {"semestre": 1, "nombre": "Química Materiales", "horas": 3, "req_lab": "SI", "target": "Lavoisier"},
    {"semestre": 1, "nombre": "Física 1", "horas": 6, "req_lab": "SI", "target": "Einstein"},
    {"semestre": 1, "nombre": "Topografía 1", "horas": 4, "req_lab": "SI", "target": "Topógrafo"},
    {"semestre": 1, "nombre": "Redacción", "horas": 2, "req_lab": "NO", "target": "Cervantes"},
    {"semestre": 1, "nombre": "Realidad Nacional", "horas": 2, "req_lab": "NO", "target": "Bernoulli"},
    {"semestre": 2, "nombre": "Cálculo Integral", "horas": 6, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 2, "nombre": "Estática", "horas": 4, "req_lab": "NO", "target": "Resistencia"},
    {"semestre": 2, "nombre": "Programación 2", "horas": 3, "req_lab": "SI", "target": "Sismología"},
    {"semestre": 2, "nombre": "Estadística", "horas": 2, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 2, "nombre": "Física 2", "horas": 6, "req_lab": "SI", "target": "Einstein"},
    {"semestre": 2, "nombre": "Topografía 2", "horas": 4, "req_lab": "SI", "target": "Topógrafo"},
    {"semestre": 3, "nombre": "Ecuaciones Dif.", "horas": 4, "req_lab": "NO", "target": "Pitágoras"},
    {"semestre": 3, "nombre": "Resistencia Mat. 1", "horas": 4, "req_lab": "NO", "target": "Resistencia"}, 
    {"semestre": 3, "nombre": "Dinámica", "horas": 4, "req_lab": "NO", "target": "Einstein"},
    {"semestre": 3, "nombre": "Ensayo Materiales 1", "horas": 5, "req_lab": "SI", "target": "Suelos"},
    {"semestre": 3, "nombre": "Hidráulica 1", "horas": 4, "req_lab": "SI", "target": "Hidráulico"},
    {"semestre": 3, "nombre": "Trazado Vías", "horas": 4, "req_lab": "SI", "target": "Vías"},
    {"semestre": 3, "nombre": "Geología", "horas": 3, "req_lab": "NO", "target": "Suelos"},
    {"semestre": 4, "nombre": "Métodos Numéricos", "horas": 4, "req_lab": "SI", "target": "Pitágoras"},
    {"semestre": 4, "nombre": "Resistencia Mat. 2", "horas": 4, "req_lab": "NO", "target": "Resistencia"}, 
    {"semestre": 4, "nombre": "Hidrología Básica", "horas": 2, "req_lab": "NO", "target": "Hidráulico"},
    {"semestre": 4, "nombre": "Ensayo Materiales 2", "horas": 5, "req_lab": "SI", "target": "Suelos"},
    {"semestre": 4, "nombre": "Hidráulica 2", "horas": 4, "req_lab": "SI", "target": "Hidráulico"},
    {"semestre": 4, "nombre": "Saneamiento Amb.", "horas": 4, "req_lab": "NO", "target": "Sanitaria"},
    {"semestre": 4, "nombre": "Mecánica Suelos 1", "horas": 6, "req_lab": "SI", "target": "Suelos"},
    {"semestre": 5, "nombre": "Concepción Arq.", "horas": 2, "req_lab": "NO", "target": "Construcción"},
    {"semestre": 5, "nombre": "Estructuras 1", "horas": 6, "req_lab": "NO", "target": "Estructuras"}, 
    {"semestre": 5, "nombre": "Hormigón Armado 1", "horas": 6, "req_lab": "NO", "target": "Hormigones"},
    {"semestre": 5, "nombre": "Diseño Hidráulico 1", "horas": 4, "req_lab": "SI", "target": "Hidráulico"},
    {"semestre": 5, "nombre": "Mecánica Suelos 2", "horas": 6, "req_lab": "SI", "target": "Suelos"},
    {"semestre": 6, "nombre": "Construcciones 1", "horas": 4, "req_lab": "SI", "target": "Construcción"}, 
    {"semestre": 6, "nombre": "Estructuras 2", "horas": 4, "req_lab": "NO", "target": "Estructuras"},
    {"semestre": 6, "nombre": "Hormigón Armado 2", "horas": 4, "req_lab": "NO", "target": "Hormigones"}, 
    {"semestre": 6, "nombre": "Diseño Hidráulico 2", "horas": 4, "req_lab": "SI", "target": "Hidráulico"},
    {"semestre": 6, "nombre": "Agua Potable", "horas": 4, "req_lab": "SI", "target": "Sanitaria"},
    {"semestre": 6, "nombre": "Mecánica Suelos 3", "horas": 4, "req_lab": "SI", "target": "Suelos"},
    {"semestre": 7, "nombre": "Construcciones 2", "horas": 4, "req_lab": "SI", "target": "Construcción"},
    {"semestre": 7, "nombre": "Estructuras 3", "horas": 4, "req_lab": "NO", "target": "Estructuras"},
    {"semestre": 7, "nombre": "Estruc. Metálicas", "horas": 4, "req_lab": "NO", "target": "Puentes"},
    {"semestre": 7, "nombre": "Hormigón Armado 3", "horas": 4, "req_lab": "NO", "target": "Hormigones"},
    {"semestre": 7, "nombre": "Vías Comunicación", "horas": 6, "req_lab": "SI", "target": "Vias"},
    {"semestre": 7, "nombre": "Alcantarillado", "horas": 4, "req_lab": "SI", "target": "Sanitaria"},
    {"semestre": 7, "nombre": "Geotecnia", "horas": 3, "req_lab": "SI", "target": "Suelos"},
    {"semestre": 8, "nombre": "Obras Civiles", "horas": 4, "req_lab": "NO", "target": "Gerencia"},
    {"semestre": 8, "nombre": "Ingeniería Económica", "horas": 2, "req_lab": "NO", "target": "Gerencia"},
    {"semestre": 8, "nombre": "Ingeniería Tránsito", "horas": 4, "req_lab": "NO", "target": "Vias"},
    {"semestre": 8, "nombre": "Impacto Amb.", "horas": 2, "req_lab": "NO", "target": "Sanitaria"},
    {"semestre": 8, "nombre": "Pavimentos", "horas": 4, "req_lab": "SI", "target": "Pavimentos"},
    {"semestre": 8, "nombre": "Admin. Empresas", "horas": 2, "req_lab": "NO", "target": "Gerencia"},
    {"semestre": 9, "nombre": "Puentes", "horas": 4, "req_lab": "NO", "target": "Puentes"},
    {"semestre": 9, "nombre": "Presupuestos", "horas": 2, "req_lab": "NO", "target": "Gerencia"},
    {"semestre": 9, "nombre": "Diseño Presas", "horas": 2, "req_lab": "NO", "target": "Hidráulico"},
    {"semestre": 9, "nombre": "Plan Tesis", "horas": 2, "req_lab": "NO", "target": "Proyectos"},
    {"semestre": 10, "nombre": "Diseño Sismorresistente", "horas": 4, "req_lab": "NO", "target": "Sismología"}, 
    {"semestre": 10, "nombre": "Fiscalización", "horas": 2, "req_lab": "NO", "target": "Gerencia"},
    {"semestre": 10, "nombre": "Tesis", "horas": 10, "req_lab": "NO", "target": "Proyectos"}
]
for m in civil: m['carrera'] = "Civil"
materias_raw.extend(civil)


# ==========================================
# 2. FUNCIONES DE CÁLCULO DINÁMICO
# ==========================================
def calcular_alumnos(semestre, carrera, es_lab):
    """
    Simula la cantidad de alumnos según el semestre.
    Semestres bajos = Más alumnos.
    Laboratorios = Grupos más pequeños.
    """
    base = 35
    if semestre <= 2: base = random.randint(45, 50)  # Masivos
    elif semestre <= 4: base = random.randint(40, 50)
    elif semestre <= 7: base = random.randint(30, 38)
    else: base = random.randint(15, 25) # Semestres finales
    
    if es_lab == "SI":
        base = int(base * 0.8) # Reducimos un 20% si es lab
    return base

# ==========================================
# 3. PROCESAMIENTO Y NORMALIZACIÓN
# ==========================================
print("🔧 Normalizando horas, laboratorios y calculando alumnos realistas...")

for m in materias_raw:
    # 1. Normalizar Horas (Pares)
    if m['horas'] % 2 != 0:
        m['horas'] += 1
        
    # 2. Regla Lab Civil (Liberar no críticas)
    if m['carrera'] == "Civil" and m['req_lab'] == "SI":
        nombre = m['nombre'].lower()
        criticas = ["ensayo", "suelos", "hidráulica", "topografía", "pavimentos", "hormigón", "cad", "química", "física", "computo"]
        if not any(k in nombre for k in criticas):
            m['req_lab'] = "NO"
            
    # 3. Asignar Alumnos (NUEVO)
    m['alumnos'] = calcular_alumnos(m['semestre'], m['carrera'], m['req_lab'])

# ==========================================
# 4. LÓGICA DE ASIGNACIÓN DOCENTE
# ==========================================
KEYWORDS_BASICAS = ["Euler", "Newton", "Lenguaje", "Curie", "Sociales", "Gauss", "Pitágoras", "Einstein", "Cervantes", "Bernoulli", "Lavoisier", "Weber", "Marx"]
GRUPO_IT = ["Sistemas", "Computación"]
GRUPO_FISICO = ["Diseño Industrial", "Civil"]

try:
    df_ing = pd.read_excel("ingenieros.xlsx")
    ing_db = {}
    carga_horaria = {}
    
    for idx, row in df_ing.iterrows():
        areas = str(row.get('carreras', '')).split(";")
        ing_db[row['id']] = {"nombre": str(row['nombre']), "areas": areas}
        carga_horaria[row['id']] = 0
except:
    print("⚠️ Error leyendo ingenieros.xlsx (Se requiere para asignar IDs).")
    ing_db = {}

lista_final = []

for i, m in enumerate(materias_raw):
    target = m.get('target', "")
    carrera_materia = m['carrera']
    docente_id = 1
    
    candidates = []
    
    # A. Detectar si es materia básica
    es_basica = any(k in target for k in KEYWORDS_BASICAS)
    
    if es_basica:
        target_group = GRUPO_IT if carrera_materia in GRUPO_IT else GRUPO_FISICO
        for id_ing, data in ing_db.items():
            if all(c in data['areas'] for c in target_group):
                candidates.append(id_ing)
    else:
        for id_ing, data in ing_db.items():
            if carrera_materia in data['areas'] and len(data['areas']) == 1:
                candidates.append(id_ing)
                
    # B. Filtro por Nombre
    perfect_matches = [id for id in candidates if target in ing_db[id]['nombre']]
    
    # C. Selección Final
    pool = perfect_matches if perfect_matches else candidates
    
    if pool:
        pool.sort(key=lambda x: carga_horaria[x])
        docente_id = pool[0]
        carga_horaria[docente_id] += m['horas']
    else:
        # Fallback
        fallback = [id for id, d in ing_db.items() if carrera_materia in d['areas']]
        if fallback:
            fallback.sort(key=lambda x: carga_horaria[x])
            docente_id = fallback[0]
            carga_horaria[docente_id] += m['horas']

    lista_final.append({
        "id": 1000 + i,
        "carrera": m['carrera'],
        "semestre": m['semestre'],
        "nombre": m['nombre'],
        "horas": m['horas'], 
        "alumnos": m['alumnos'], # Dato calculado
        "req_lab": m['req_lab'],
        "docente_id": docente_id
    })

df = pd.DataFrame(lista_final)
df.to_excel("materias.xlsx", index=False)
print("✅ 'materias.xlsx' generado COMPLETAMENTE.")
print("   - Todas las carreras incluidas.")
print("   - Alumnos calculados dinámicamente (60 a 20 según nivel).")
print("   - Docentes asignados y segregados.")