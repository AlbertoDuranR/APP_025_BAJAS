import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import NamedStyle

class excelUtils:
    # Función para limpiar el archivo Excel
    def cleanExcel(self, filePath):
        # Leer el archivo Excel
        df = pd.read_excel(filePath, dtype=str)

        # Eliminar filas que contienen "Total" o "Filtros aplicados"
        df_cleaned = df[~df.iloc[:, 0].str.contains('Total|Filtros aplicados', na=False)].copy()

        # Formatear columna 'Fecha' si existe
        if 'Fecha' in df_cleaned.columns:
            df_cleaned['Fecha'] = pd.to_datetime(df_cleaned['Fecha'], errors='coerce').dt.strftime('%d/%m/%Y')

        return df_cleaned

    # Función para guardar los datos limpiados
    def saveCleanedData(self, df_cleaned, filePath):
        df_cleaned.to_excel(filePath, index=False, engine='openpyxl')

    # Función para aplicar formato "Texto" a todas las celdas
    def applyTextFormat(self, filePath):
        # Cargar el archivo con openpyxl
        wb = load_workbook(filePath)
        ws = wb.active

        # Crear estilo de texto
        text_style = NamedStyle(name="text_style", number_format="@")  # Formato "Texto"

        # Aplicar el formato a todas las celdas
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                cell.style = text_style

        # Guardar el archivo con el formato aplicado
        wb.save(filePath)