# 🎓 OptiSchedule: Sistema de Planificación Inteligente de Horarios

**OptiSchedule** es una aplicación web basada en Python diseñada para automatizar y optimizar la generación de horarios universitarios complejos. Utiliza programación lineal (Linear Programming) para asignar materias, docentes y aulas, garantizando que no existan conflictos de tiempo, espacio o recursos humanos.

---

## 🚀 Características Principales

* **Optimización Matemática:** Utiliza la librería `PuLP` (Solver CBC) para encontrar la solución óptima matemática, no por tanteo.
* **Gestión Multi-Carrera:** Soporta la generación simultánea de horarios para múltiples carreras (Sistemas, Civil, Computación, Diseño) compartiendo recursos.
* **Segregación de Docentes:** Distingue entre profesores de "Ciencias Básicas" (compartidos) y "Especialistas" (exclusivos por carrera).
* **Control de Infraestructura:** Gestiona aulas teóricas y laboratorios especializados, evitando la sobreocupación.
* **Exportación:** Generación de reportes en Excel y PDF listos para imprimir.

---

## 📂 Estructura del Proyecto

A continuación se describe la función de cada archivo en el proyecto:

### 🔹 Núcleo de la Aplicación
* **`app.py`**: Punto de entrada principal. Contiene la interfaz de usuario (UI) en Streamlit, el menú lateral y la lógica de navegación.
* **`motor.py`**: **El cerebro del sistema.** Contiene el algoritmo de optimización con `PuLP`. Define las variables de decisión y las restricciones matemáticas.
* **`config.py`**: Archivo de configuración global. Define constantes como los días de la semana, franjas horarias permitidas y rutas de archivos.
* **`funciones.py`**: Funciones auxiliares para la carga de datos, limpieza de strings y validaciones previas.
* **`reportes.py`**: Módulo encargado de tomar los datos generados y convertirlos en archivos descargables (PDF con diseño formal y Excel).


### 🔹 Datos y Generadores (`/datos`)
Esta carpeta contiene los datos de entrada y los scripts para fabricar datos de prueba robustos:
* **`aulas.xlsx`**: Inventario de infraestructura (Aulas teóricas, Laboratorios de Cómputo, Talleres).
* **`ingenieros.xlsx`**: Base de datos de docentes con sus especialidades y disponibilidad horaria.
* **`materias.xlsx`**: Malla curricular completa con requisitos de horas, laboratorios y docentes sugeridos.
* **`generar_*.py`**: Scripts de Python utilizados para crear o resetear los archivos Excel base con datos normalizados (ej. corregir horas impares, asignar cargas equilibradas).

---

## 🧠 Lógica de Optimización (Restricciones)

El motor (`motor.py`) resuelve el horario aplicando las siguientes reglas estrictas ("Hard Constraints"):

1.  **R1 - Cumplimiento Académico:** Cada materia debe impartirse exactamente la cantidad de horas semanales requeridas en el plan de estudios.
2.  **R2 - Unicidad de Espacio:** Un aula no puede tener dos clases diferentes asignadas en el mismo día y hora.
3.  **R3 - Ubicuidad Docente:** Un profesor no puede estar en dos lugares al mismo tiempo.
4.  **R4 - No Clonación de Estudiantes (La Regla de Oro):** Un grupo de estudiantes de un mismo semestre (ej. "Civil Semestre 2") no puede tener dos materias asignadas simultáneamente.
5.  **R5 - Competencia Docente:**
    * Profesores del "Grupo IT" solo dan clases en Sistemas/Computación.
    * Profesores del "Grupo Físico" solo dan clases en Civil/Diseño.
    * Especialistas solo dan materias de su rama específica.
6.  **R6 - Infraestructura Adecuada:** Si una materia requiere laboratorio (`req_lab="SI"`), el algoritmo forzosamente buscará un aula de `tipo="LAB"`.

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.10+**: Lenguaje base.
* **Streamlit**: Framework para la interfaz web interactiva.
* **Pandas**: Manipulación y análisis de datos estructurados.
* **PuLP**: Librería de modelado de optimización lineal.
* **OpenPyXL**: Lectura y escritura de archivos Excel.

---

## ⚙️ Instalación y Ejecución

1.  **Clonar el repositorio o descargar la carpeta.**
2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ejecutar la aplicación:**
    ```bash
    python -m streamlit run app.py
    ```

---

## 🐛 Solución de Problemas Comunes

* **Error "Infeasible":** Significa que no hay solución matemática posible.
    * *Causa:* Faltan aulas, faltan profesores o una materia tiene horas impares (3h/5h) que no encajan en bloques pares.
    * *Solución:* Usar los scripts `generar_*.py` para normalizar las horas a pares y aumentar la infraestructura.
* **Error de Docente no encontrado:** Asegúrese de que el nombre "target" en `materias.xlsx` coincida parcialmente con el nombre real en `ingenieros.xlsx`.