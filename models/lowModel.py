from utils.excelUtils import excelUtils

class LowModel:

    def __init__(self) -> None:
        self.excel = excelUtils()  # Instancia de excelUtils

    def fileCleanup(self, filePath):
        try:
            # 1. Leer y limpiar el archivo Excel
            df_cleaned = self.excel.cleanExcel(filePath)

            # 2. Guardar los datos limpiados de vuelta en el archivo
            self.excel.saveCleanedData(df_cleaned, filePath)

            # 3. Aplicar formato de "Texto" a todas las celdas
            self.excel.applyTextFormat(filePath)

            print(f"Archivo {filePath} limpiado y formateado correctamente.")
            return {'success': True, 'message': 'Archivo limpiado y formateado correctamente.'}
        
        except Exception as e:
            print(f"Error al limpiar y formatear el archivo: {str(e)}")
            return {'success': False, 'message': f'Error al limpiar y formatear el archivo: {str(e)}'}



    # crear archivo acepta
    def createFileAcepta(self, urlFile):
        pass

    # crear archivo sunat
    def createFileSunat(self, urlFile):
        pass