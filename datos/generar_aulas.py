import pandas as pd

# LISTADO DE AULAS REAL (Base proporcionada + Expansión a 60)
data_aulas = [
    # =================================================================
    # 1. LABORATORIOS DE SISTEMAS / COMPUTACIÓN (13 Espacios)
    # =================================================================
    {"nombre": "LAB 1", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB 2", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB 3", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB 4", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB 5", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB 6", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB 7", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB 8", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB 9 (NUEVO)", "capacidad": 40, "tipo": "LAB"},  # Agregado
    {"nombre": "LAB 10 (NUEVO)", "capacidad": 40, "tipo": "LAB"}, # Agregado
    {"nombre": "LAB 11", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB 12", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB 13", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB SUFICIENCIA A", "capacidad": 45, "tipo": "LAB"},
    {"nombre": "LAB SUFICIENCIA B", "capacidad": 45, "tipo": "LAB"},
    {"nombre": "LAB REDES", "capacidad": 35, "tipo": "LAB"},
    
    # =================================================================
    # 2. BLOQUE A - TEORÍA (8 Espacios)
    # =================================================================
    {"nombre": "A1-1", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "A1-4", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "A2-5", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "A2-6", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "A2-7", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "A2-8", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "A2-9", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "A3-22", "capacidad": 50, "tipo": "TEORIA"},

    # =================================================================
    # 3. SALAS POSGRADO (7 Espacios - Uso flexible)
    # =================================================================
    {"nombre": "SALA A POSGRADO", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "SALA B POSGRADO", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "A4-2 POSGRADO", "capacidad": 45, "tipo": "TEORIA"},
    {"nombre": "A4-3 POSGRADO", "capacidad": 45, "tipo": "TEORIA"},
    {"nombre": "A4-4 POSGRADO", "capacidad": 45, "tipo": "TEORIA"},
    {"nombre": "A4-5 POSGRADO", "capacidad": 45, "tipo": "TEORIA"},
    {"nombre": "A4-6 POSGRADO", "capacidad": 45, "tipo": "TEORIA"},

    # =================================================================
    # 4. COMPLEJO CIVIL / MECÁNICA / FÍSICA (16 Espacios)
    # =================================================================
    {"nombre": "CAPACITACION SALA 1 CIVIL", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "CAPACITACION SALA 2 CIVIL", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "CAPACITACION SALA 3 CIVIL", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "LAB COMPUTO CIVIL SALA A", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB COMPUTO CIVIL SALA C", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "LAB COMPUTO CIVIL SALA E", "capacidad": 40, "tipo": "LAB"},
    {"nombre": "A3-14 (CIV)", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "A3-15 (CIV)", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "A3-16 (CIV)", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "A3-17 (CIV)", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "AULA ING MECANICA", "capacidad": 50, "tipo": "TEORIA"},
    {"nombre": "UNIDAD DE FISICA", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "LAB FISICA 2", "capacidad": 35, "tipo": "LAB"},
    {"nombre": "LAB FISICA CG", "capacidad": 35, "tipo": "LAB"},
    {"nombre": "LAB SUELOS Y MATERIALES", "capacidad": 30, "tipo": "LAB"},
    {"nombre": "LAB HIDRAULICA (NUEVO)", "capacidad": 30, "tipo": "LAB"}, # Agregado para Civil

    # =================================================================
    # 5. BLOQUE B - NUEVO (Expansión Teórica) (10 Espacios)
    # =================================================================
    {"nombre": "AULA B-1 (Bloque Nuevo)", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "AULA B-2 (Bloque Nuevo)", "capacidad": 60, "tipo": "TEORIA"},
    # --- Aulas añadidas para llegar a 60 ---
    {"nombre": "AULA B-3 (Bloque Nuevo)", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "AULA B-4 (Bloque Nuevo)", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "AULA B-5 (Bloque Nuevo)", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "AULA B-6 (Bloque Nuevo)", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "AULA B-7 (Bloque Nuevo)", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "AULA B-8 (Bloque Nuevo)", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "AULA B-9 (Bloque Nuevo)", "capacidad": 60, "tipo": "TEORIA"},
    {"nombre": "AULA B-10 (Bloque Nuevo)", "capacidad": 60, "tipo": "TEORIA"},

    # =================================================================
    # 6. TALLERES Y VIRTUALES (6 Espacios)
    # =================================================================
    {"nombre": "LAB VIRTUAL 1 SI", "capacidad": 200, "tipo": "LAB"},
    {"nombre": "LAB VIRTUAL 2 SI", "capacidad": 200, "tipo": "LAB"},
    {"nombre": "AULA VIRTUAL DISEÑO IND", "capacidad": 200, "tipo": "TEORIA"},
    {"nombre": "TALLER DE DIBUJO 1", "capacidad": 30, "tipo": "LAB"},
    {"nombre": "TALLER DE DIBUJO 2", "capacidad": 30, "tipo": "LAB"},
    {"nombre": "AULA MAGNA (Compartida)", "capacidad": 100, "tipo": "TEORIA"},
]

# Asignar IDs únicos automáticamente
for i, aula in enumerate(data_aulas):
    aula['id'] = 2000 + i

df = pd.DataFrame(data_aulas)
df.to_excel("aulas.xlsx", index=False)
print(f"✅ Aulas generadas correctamente (aulas.xlsx). Total espacios: {len(data_aulas)}")
print("   - Se han agregado aulas del 'Bloque B' y Laboratorios extra para descongestionar.")