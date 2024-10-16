from utils.excelUtils import excelUtils
from utils.responseBuilder import responseBuilder
from flask import send_file, Response, jsonify
import zipfile

import pandas as pd
import os

class LowModel:

    def __init__(self) -> None:
        self.excel = excelUtils()  # Instancia de excelUtils

    # limpieza del archivo excel cargado
    def fileCleanup(self,upload_folder, filePath, period, functionApp):
        try:
            # 0. Eliminar carpetas de dias anteriores
            

            # 1. Leer y limpiar el archivo Excel
            df_cleaned = self.excel.cleanExcel(filePath)

            # 2. Filtrar las filas por el período (YYYY-MM)
            if functionApp == "low":
                df_cleaned = self.excel.filterByPeriod(df_cleaned, period)

            # 3. Guardar los datos limpiados y filtrados en el archivo
            self.excel.saveCleanedData(df_cleaned, filePath)

            # 4. Aplicar formato de "Texto" a todas las celdas
            self.excel.applyTextFormat(filePath)

            # 5. Devolver cantidad de filas filtradas y ruta del archivo
            num_rows = df_cleaned.shape[0]

            # devolver el mensaje de correcto y la ruta
            return responseBuilder.success('Archivo creado correctamente', {'upload_folder': upload_folder ,'file_path': filePath, 'number_rows': num_rows})
        
        except Exception as e:
            # print(f"Error al limpiar y filtrar el archivo: {str(e)}")
            return responseBuilder.error(f'Error al limpiar y filtrar el archivo: {str(e)}')


    # crear archivo acepta
    def createFileAcepta(self, filePath):
        try:
            # 1. Leer y procesar el archivo Excel
            df_acepta = self.excel.process_excel_file(filePath)

            # 2. Asumir que la carpeta 'acepta' ya existe
            output_dir = self.excel.get_output_directory(filePath)

            # 3. Dividir y guardar en archivos CSV 45 items
            num_parts = self.excel.split_and_save_csv_by_day(df_acepta, output_dir)

            return responseBuilder.success(f'{num_parts} archivos Acepta creados correctamente.', {'folder_path': output_dir})

        except Exception as e:
            return responseBuilder.error(f'Error al crear los archivos Acepta: {str(e)}')


    # crear archivo sunat
    def createFileSunat(self, filePath):
        try:
            # 1. Leer y procesar el archivo Excel
            df_sunat = self.excel.process_excel_file_sunat(filePath)

            # 2. Obtener la carpeta 'sunat' ya existente
            output_dir = self.excel.get_output_directory_sunat(filePath)

            # 3. Dividir y guardar en archivos TXT
            num_parts = self.excel.split_and_save_txt(df_sunat, output_dir)

            return responseBuilder.success(f'{num_parts} archivos SUNAT creados correctamente.', {'folder_path': output_dir})

        except Exception as e:
            return responseBuilder.error(f'Error al crear los archivos SUNAT: {str(e)}')
    

    def downloadFiles(self, folder_path):
        try:
            zip_filename = "archivos_sunat.zip"
            zip_path = os.path.join(folder_path, zip_filename)

            # Crear el archivo ZIP
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        # Excluir el archivo ZIP de ser añadido al propio ZIP
                        if file != zip_filename:
                            zipf.write(file_path, os.path.basename(file_path))

            # Verificar si el archivo ZIP fue creado exitosamente
            if os.path.exists(zip_path):
                # retonrar el archio
                return send_file(zip_path, as_attachment=True)
        
            else:
                return jsonify({"message": "Error al descargar"})  # No se pudo crear el ZIP

        except Exception as e:
            return jsonify({"message": "falso", "error": str(e)}), 500  # Hubo un error durante el proceso