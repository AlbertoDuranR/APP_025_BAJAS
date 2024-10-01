from utils.excelUtils import excelUtils

class LowModel:

    def __init__(self) -> None:
        self.excel = excelUtils()  # Instancia de excelUtils

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

            # print(f"Archivo {filePath} limpiado, filtrado y formateado correctamente.")
            return {'success': True, 'message': 'Archivo limpiado, filtrado y formateado correctamente.'}
        
        except Exception as e:
            # print(f"Error al limpiar y filtrar el archivo: {str(e)}")
            return {'success': False, 'message': f'Error al limpiar y filtrar el archivo: {str(e)}'}

    # crear archivo acepta
    def createFileAcepta(self, urlFile):
        pass

    # crear archivo sunat
    def createFileSunat(self, urlFile):
        pass