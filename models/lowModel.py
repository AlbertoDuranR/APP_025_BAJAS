from utils.excelUtils import excelUtils
from utils.responseBuilder import responseBuilder

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

            # devolver el mensaje de correcto y la ruta
            return responseBuilder.success('Archivo creado correctamente', {'file_path': filePath})
        
        except Exception as e:
            # print(f"Error al limpiar y filtrar el archivo: {str(e)}")
            return responseBuilder.error(f'Error al limpiar y filtrar el archivo: {str(e)}')

    # crear archivo acepta
    def createFileAcepta(self, urlFile):
        pass

    # crear archivo sunat
    def createFileSunat(self, urlFile):
        pass