import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import NamedStyle
import os

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

    # Generar Archivo para Acepta
    def process_excel_file(self, filePath):
        # Leer el archivo Excel y procesar las columnas
        df = pd.read_excel(filePath, dtype=str)
        df['Serie1-Serie2'] = df['Serie1'] + '-' + df['Serie2']
        df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
        df_acepta = df[['TipoDocumento', 'Serie1-Serie2', 'Fecha']].copy()
        df_acepta.loc[:, 'Error'] = 'Error en Sistema'
        return df_acepta


    def get_output_directory(self, filePath):
        # Obtener la ruta de la carpeta 'acepta' (ya existente)
        output_dir = os.path.join(os.path.dirname(filePath), 'acepta')
        return output_dir
    

    def split_and_save_csv(self, df_acepta, output_dir, rows_per_file=45):
        # Dividir el DataFrame en partes y guardar en archivos CSV
        num_parts = (len(df_acepta) // rows_per_file) + (1 if len(df_acepta) % rows_per_file != 0 else 0)
        for i in range(num_parts):
            part_df = df_acepta.iloc[i * rows_per_file:(i + 1) * rows_per_file]
            output_path = os.path.join(output_dir, f'acepta_{i + 1}.csv')
            part_df.to_csv(output_path, sep=';', index=False, header=False)
        return num_parts
    
    # Generar archivo para sunat
    def process_excel_file_sunat(self, filePath):
        df = pd.read_excel(filePath, dtype=str)
        df_sunat = df[['Empresa', 'TipoDocumento', 'Serie1', 'Serie2', 'Fecha', 'Importe Total']].copy()
        return df_sunat

    def get_output_directory_sunat(self, filePath):
        return os.path.join(os.path.dirname(filePath), 'sunat')

    def split_and_save_txt(self, df_sunat, output_dir, rows_per_file=45):
        num_parts = (len(df_sunat) // rows_per_file) + (1 if len(df_sunat) % rows_per_file != 0 else 0)
        for i in range(num_parts):
            part_df = df_sunat.iloc[i * rows_per_file:(i + 1) * rows_per_file]
            output_path = os.path.join(output_dir, f'sunat_{i + 1}.txt')
            part_df.to_csv(output_path, sep='|', index=False, header=False)
        return num_parts