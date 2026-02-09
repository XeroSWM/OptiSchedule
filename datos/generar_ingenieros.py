import pandas as pd
import random

# ==============================================================================
# CONFIGURACIÓN DE TIEMPO (DISPONIBILIDAD TOTAL)
# ==============================================================================
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS = ["07:00-09:00", "09:00-11:00", "11:00-13:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]
ALL_SLOTS = [f"{d} {h}" for d in DIAS for h in HORAS]

lista_final = []
id_counter = 1

def crear_docente(nombre, areas_str):
    global id_counter
    # ESTRATEGIA: Disponibilidad Masiva (Casi tiempo completo)
    # Esto elimina el error "Infeasible" por falta de horario del profesor.
    slots = ALL_SLOTS.copy()
    random.shuffle(slots)
    
    # Quitamos solo 2 bloques aleatorios para dar un toque de realismo
    # pero asegurando que tengan ~28 slots (56 horas) disponibles.
    slots = slots[:28] 
    
    docente = {
        "id": id_counter,
        "nombre": nombre,
        "carreras": areas_str,
        "disponibilidad": ";".join(slots)
    }
    id_counter += 1
    return docente

# ==============================================================================
# 1. GRUPO BÁSICAS IT (Sistemas y Computación) - 6 Docentes
# ==============================================================================
grupo_it = [
    "Mat. Juan Euler (IT)", 
    "Fís. Isaac Newton (IT)", 
    "Lic. Ana Lenguaje (IT)", 
    "Quim. Marie Curie (IT)",
    "Est. Gauss Normal (IT)",
    "Dr. Sociales Marx (IT)"
]
for n in grupo_it: 
    lista_final.append(crear_docente(n, "Sistemas;Computación"))

# ==============================================================================
# 2. GRUPO BÁSICAS FÍSICO (Diseño y Civil) - 6 Docentes
# ==============================================================================
# Nombres alineados con los targets de la malla de Civil
grupo_fis = [
    "Mat. Pitágoras (Civil/Dis)", 
    "Fís. Einstein (Civil/Dis)", 
    "Lic. Cervantes (Civil/Dis)", 
    "Est. Bernoulli (Civil/Dis)",
    "Quim. Lavoisier (Civil/Dis)",
    "Dr. Weber (Civil/Dis)"
]
for n in grupo_fis: 
    lista_final.append(crear_docente(n, "Diseño Industrial;Civil"))

# ==============================================================================
# 3. ESPECIALISTAS SISTEMAS (12 Docentes)
# ==============================================================================
sistemas = [
    "Ing. Carlos Desarrollo", "Dra. Lucia Datos", "Ing. Sofia Seguridad", 
    "Ing. Web Master", "Msc. Gestión TIC", "Ing. Diana DevOps", 
    "Msc. Pedro Cloud", "Dr. Mario Inteligencia", "Ing. Roberto Moviles", 
    "Ing. Ana Testing", "Msc. Luis Agile", "Ing. Karla UX/UI"
]
for n in sistemas: lista_final.append(crear_docente(n, "Sistemas"))

# ==============================================================================
# 4. ESPECIALISTAS COMPUTACIÓN (12 Docentes)
# ==============================================================================
compu = [
    "Dr. Alan Turing", "Ing. Grace Hopper", "Ing. Linus Torvalds", 
    "Msc. Redes Cisco", "Dr. Von Neumann", "Ing. Ada Lovelace", 
    "Msc. Ken Thompson", "Ing. Tim Berners", "Dr. Marvin Minsky", 
    "Ing. Margaret Hamilton", "Ing. Dennis Ritchie", "Msc. Claude Shannon"
]
for n in compu: lista_final.append(crear_docente(n, "Computación"))

# ==============================================================================
# 5. ESPECIALISTAS DISEÑO INDUSTRIAL (12 Docentes)
# ==============================================================================
diseno = [
    "Dis. Leonardo Da Vinci", "Arq. Walter Bauhaus", "Ing. Materiales Pro", 
    "Msc. Ergonomía User", "Dis. Zaha Hadid", "Ing. CAD Master", 
    "Lic. Historia Arte", "Msc. Eco Diseño", "Ing. Procesos Fab", 
    "Dis. Dieter Rams", "Ing. Textil Moda", "Arq. Frank Lloyd"
]
for n in diseno: lista_final.append(crear_docente(n, "Diseño Industrial"))

# ==============================================================================
# 6. ESPECIALISTAS CIVIL (14 Docentes - SOLUCIÓN DEL CUELLO DE BOTELLA)
# ==============================================================================
# Aquí desglosamos "Estructuras" en varios roles para que nadie se sature.
civil = [
    "Ing. Estructuras Top",      # Encargado de Estructuras 1, 2, 3
    "Ing. Hormigones Mix",       # Encargado de Hormigón 1, 2, 3
    "Ing. Resistencia Mat",      # Encargado de Estática y Resistencias
    "Ing. Hidráulico Water",     # Hidráulica y Fluidos
    "Ing. Sanitaria Amb",        # Sanitaria y Ambiental
    "Ing. Vías Caminos",         # Vías
    "Ing. Pavimentos Mix",       # Pavimentos (Ayuda a Vías)
    "Ing. Mecánica Suelos",      # Suelos y Geotecnia
    "Ing. Topógrafo Geo",        # Topografía
    "Arq. Construcción",         # Dibujo y Construcciones
    "Ing. Gerencia Obra",        # Presupuestos, Fiscalización, Admin
    "Msc. Puentes Grandes",      # Puentes y Metálicas
    "Ing. Sismología",           # Sismorresistencia
    "Ing. Proyectos Tesis"       # Titulación
]
for n in civil: lista_final.append(crear_docente(n, "Civil"))

# GUARDAR
df = pd.DataFrame(lista_final)
df.to_excel("ingenieros.xlsx", index=False)

print(f"✅ 'ingenieros.xlsx' generado CORRECTAMENTE.")
print(f"📊 Total Docentes: {len(lista_final)}")
print("   - Solución Civil: Se han creado 14 roles específicos (Hormigones, Resistencia, Gerencia...)")
print("   - Esto evita que 'Ing. Estructuras' tenga 80 horas de clase y bloquee el horario.")