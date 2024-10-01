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


        return df_cleaned
    
    def filterByPeriod(self, df, period):
        """
        Filtrar las filas que coincidan con el período proporcionado.
        El período debe estar en formato 'YYYY-MM'.
        """
        try:
            # Asegurar que la columna de Fecha existe
            if 'Fecha' not in df.columns:
                raise ValueError("No se encontró la columna 'Fecha' en el archivo.")

            # Convertir la columna 'Fecha' a datetime (si no lo es)
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

            # Extraer el período en formato 'YYYY-MM' de la columna 'Fecha'
            df['Periodo'] = df['Fecha'].dt.strftime('%Y-%m')

            # Filtrar las filas que coincidan con el período proporcionado
            df_filtered = df[df['Periodo'] == period].copy()

            # Eliminar la columna 'Periodo' ya que no es necesaria en el archivo final
            df_filtered.drop(columns=['Periodo'], inplace=True)


            df_filtered['Fecha'] = pd.to_datetime(df_filtered['Fecha'], errors='coerce').dt.strftime('%d/%m/%Y')

            return df_filtered

        except Exception as e:
            print(f"Error al filtrar por período: {str(e)}")
            raise

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