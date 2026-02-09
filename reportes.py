import pandas as pd
import io
from xlsxwriter import Workbook

# Librerías para PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Importamos configuración global
from config import DIAS, HORAS

def generar_excel_inteligente(df_horario):
    """
    Genera un archivo Excel con múltiples vistas (Semestre, Docente, Aulas).
    Retorna un objeto BytesIO listo para descargar.
    """
    output = io.BytesIO()
    
    # Configuramos el escritor de Excel
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Estilos
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#4F81BD',
            'font_color': 'white',
            'border': 1
        })
        
        # ---------------------------------------------------------
        # PESTAÑA 1: POR SEMESTRE (Vista Clásica)
        # ---------------------------------------------------------
        if not df_horario.empty:
            df_semestre = df_horario.sort_values(by=['Carrera', 'Semestre', 'Día', 'Hora'])
            df_semestre.to_excel(writer, sheet_name='Por Semestre', index=False)
            
            worksheet1 = writer.sheets['Por Semestre']
            for col_num, value in enumerate(df_semestre.columns.values):
                worksheet1.write(0, col_num, value, header_format)
                worksheet1.set_column(col_num, col_num, 20)

        # ---------------------------------------------------------
        # PESTAÑA 2: POR DOCENTE (VISTA GENERAL)
        # ---------------------------------------------------------
        if not df_horario.empty:
            # Agrupamos por Docente para ver su carga total
            df_docente = df_horario.sort_values(by=['Docente', 'Día', 'Hora'])
            
            # Reordenamos columnas
            cols = ['Docente', 'Materia', 'Día', 'Hora', 'Aula', 'Carrera', 'Semestre']
            # Filtramos columnas que existan
            cols_existentes = [c for c in cols if c in df_docente.columns]
            df_docente = df_docente[cols_existentes]
            
            df_docente.to_excel(writer, sheet_name='Por Docente (General)', index=False)
            
            worksheet2 = writer.sheets['Por Docente (General)']
            for col_num, value in enumerate(df_docente.columns.values):
                worksheet2.write(0, col_num, value, header_format)
                worksheet2.set_column(col_num, col_num, 25)

        # ---------------------------------------------------------
        # PESTAÑA 3: OCUPACIÓN DE AULAS
        # ---------------------------------------------------------
        if not df_horario.empty:
            df_aulas = df_horario.sort_values(by=['Aula', 'Día', 'Hora'])
            cols_aula = ['Aula', 'Día', 'Hora', 'Materia', 'Docente', 'Semestre']
            cols_existentes_aula = [c for c in cols_aula if c in df_aulas.columns]
            df_aulas = df_aulas[cols_existentes_aula]
            
            df_aulas.to_excel(writer, sheet_name='Ocupación Aulas', index=False)
            
            worksheet3 = writer.sheets['Ocupación Aulas']
            for col_num, value in enumerate(df_aulas.columns.values):
                worksheet3.write(0, col_num, value, header_format)
                worksheet3.set_column(col_num, col_num, 20)

    output.seek(0)
    return output

def generar_pdf_horario(df_datos, titulo_reporte, carrera_nombre, modo="Semestre"):
    """
    Genera un PDF con el horario.
    - modo="Semestre": Crea una página por cada Semestre (Ideal para alumnos).
    - modo="Docente": Crea una página por cada Docente con TODA su carga (Ideal para RRHH/Profes).
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # --- Estilos Personalizados ---
    title_style = ParagraphStyle('UceTitle', parent=styles['Heading1'], fontSize=16, leading=20, alignment=1, textColor=colors.darkblue)
    career_style = ParagraphStyle('CareerSub', parent=styles['Normal'], fontSize=12, leading=14, alignment=1, spaceAfter=2)
    report_style = ParagraphStyle('ReportTitle', parent=styles['Normal'], fontSize=11, leading=13, alignment=1, spaceAfter=10, textColor=colors.grey)
    group_header_style = ParagraphStyle('GroupHeader', parent=styles['Heading2'], fontSize=14, leading=16, alignment=0, textColor=colors.darkred, spaceBefore=5, spaceAfter=10)
    cell_style = ParagraphStyle('CellStyle', parent=styles['Normal'], fontSize=7, leading=8, alignment=1)

    # 1. DETERMINAR CÓMO AGRUPAR (POR SEMESTRE O POR DOCENTE)
    if modo == "Docente":
        if 'Docente' in df_datos.columns:
            items_agrupacion = sorted(df_datos['Docente'].unique())
        else:
            items_agrupacion = ["Docente Desconocido"]
    else:
        # Modo Semestre (Default)
        if 'Semestre' in df_datos.columns:
            items_agrupacion = sorted(df_datos['Semestre'].unique())
        else:
            items_agrupacion = [1]

    # --- GENERAR PÁGINAS ---
    for i, item in enumerate(items_agrupacion):
        
        # Filtrar datos según el modo
        if modo == "Docente":
            df_slice = df_datos[df_datos['Docente'] == item]
            texto_encabezado = f"DOCENTE: {item}"
        else:
            df_slice = df_datos[df_datos['Semestre'] == item]
            texto_encabezado = f"SEMESTRE {item}"

        # Encabezado Institucional
        elements.append(Paragraph("UNIVERSIDAD CENTRAL DEL ECUADOR", title_style))
        elements.append(Paragraph("FACULTAD DE INGENIERÍA Y CIENCIAS APLICADAS", career_style))
        elements.append(Paragraph(f"CARRERA DE {carrera_nombre.upper()}", career_style))
        elements.append(Paragraph(f"<b>{titulo_reporte}</b>", report_style))
        
        # Título del Grupo (Semestre X o Docente X)
        elements.append(Paragraph(f"<b>{texto_encabezado}</b>", group_header_style))

        # Construir Matriz
        headers = ["HORA"] + DIAS
        grid_data = []
        grid_data.append(headers)
        
        for h in HORAS:
            fila = [h]
            for d in DIAS:
                # Buscar clases en este hueco
                clases = df_slice[(df_slice['Día'] == d) & (df_slice['Hora'] == h)]
                
                if not clases.empty:
                    texto_celda = ""
                    for _, info in clases.iterrows():
                        materia = info.get('Materia', 'N/A')
                        aula = info.get('Aula', 'N/A')
                        
                        # CONTENIDO DE CELDA DINÁMICO
                        if modo == "Docente":
                            # Si es reporte por docente, mostramos la Materia y el Semestre/Carrera
                            semestre = info.get('Semestre', '?')
                            texto_celda += f"<b>{materia}</b><br/>Sem: {semestre}<br/>{aula}<br/><br/>"
                        else:
                            # Si es reporte por semestre, mostramos Materia y Docente
                            docente = info.get('Docente', 'N/A')
                            texto_celda += f"<b>{materia}</b><br/>{aula}<br/><i>{docente}</i><br/><br/>"
                    
                    fila.append(Paragraph(texto_celda, cell_style))
                else:
                    fila.append("")
            grid_data.append(fila)

        # Configurar Tabla
        col_widths = [1.2 * inch] + [1.75 * inch] * 5
        t = Table(grid_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ROWBACKGROUNDS', (1, 0), (-1, -1), [colors.whitesmoke, colors.white]),
        ]))
        
        elements.append(t)
        
        # Salto de página entre gruposs
        if i < len(items_agrupacion) - 1:
            elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer