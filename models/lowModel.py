from utils.excelUtils import excelUtils
from utils.responseBuilder import responseBuilder

import pandas as pd
import os

class LowModel:

    def __init__(self) -> None:
        self.excel = excelUtils()  # Instancia de excelUtils

    # limpieza del archivo excel cargado
    def fileCleanup(self, filePath, period):
        try:
            # 1. Leer y limpiar el archivo Excel
            df_cleaned = self.excel.cleanExcel(filePath)

            # 2. Filtrar las filas por el período (YYYY-MM)
            df_cleaned = self.excel.filterByPeriod(df_cleaned, period)

            # 3. Guardar los datos limpiados y filtrados en el archivo
            self.excel.saveCleanedData(df_cleaned, filePath)

            # 4. Aplicar formato de "Texto" a todas las celdas
            self.excel.applyTextFormat(filePath)

            # devolver el mensaje de correcto y la ruta
            return responseBuilder.success('Archivo creado correctamente', {'file_path': filePath})
        
        except Exception as e:
            # print(f"Error al limpiar y filtrar el archivo: {str(e)}")
            return responseBuilder.error(f'Error al limpiar y filtrar el archivo: {str(e)}')


    # crear archivo acepta
    def createFileAcepta(self, filePath):
        try:
            # 1. Leer el archivo Excel
            df = pd.read_excel(filePath, dtype=str)

            # 2. Crear una nueva columna 'Serie1-Serie2'
            df['Serie1-Serie2'] = df['Serie1'] + '-' + df['Serie2']

            # 3. Asegurarse de que la columna Fecha esté en el formato adecuado (YYYY-MM-DD)
            df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')

            # 4. Seleccionar las columnas en el orden adecuado y crear una copia
            df_acepta = df[['TipoDocumento', 'Serie1-Serie2', 'Fecha']].copy()

            # 5. Usar .loc para agregar una nueva columna con el valor constante "Error en Sistema"
            df_acepta.loc[:, 'Error'] = 'Error en Sistema'

            # 6. Renombrar las columnas para coincidir con el formato solicitado
            df_acepta.columns = ['TipoDocumento', 'Serie1-Serie2', 'Fecha', 'Error']

            # 7. Guardar el DataFrame como un archivo CSV separado por ;
            output_path = os.path.splitext(filePath)[0] + '_acepta.csv'
            df_acepta.to_csv(output_path, sep=';', index=False, header=False)

            # Retornar éxito y ruta del archivo generado
            return {'success': True, 'message': 'Archivo Acepta creado correctamente.', 'file_path': output_path}

        except Exception as e:
            return {'success': False, 'message': f'Error al crear el archivo Acepta: {str(e)}'}

    # crear archivo sunat
    def createFileSunat(self, urlFile):
        pass