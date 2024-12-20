from flask import Blueprint, render_template, request, send_file
from models.lowModel import LowModel
from utils.urlFileUtils import UrlFile
from utils.responseBuilder import responseBuilder
import os

low = Blueprint('low', __name__)

# Inicializar el objeto urlFile y LowModel
urlFile = UrlFile()
model = LowModel()

# Ruta para la plantilla HTML
@low.route('/', methods=['GET'])
def process_index():
    return render_template('low.html')


# Cargar archivo Excel
@low.route('/upload', methods=['POST'])
def upload():
    # Verificar si se ha enviado un archivo en la petición
    file = request.files.get('file')
    period = request.form.get('period')
    functionApp = request.form.get('functionApp')


    if not file:
        return responseBuilder.error('No se cargó ningún archivo')


    try:
        # limpiar carpeta
        urlFile.deleteOldFolders()

        # Crear la carpeta para almacenar el archivo
        upload_folder = urlFile.getUploadFolder(functionApp)
        
        # Guardar el archivo subido en la carpeta creada
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Limpiar el archivo para Acepta y filtrar por el período
        return model.fileCleanup(upload_folder, file_path, period, functionApp)
       
    except Exception as e:
        # Manejo de errores durante el proceso de carga de archivos
        return responseBuilder.error(f'Ocurrió un error al procesar el archivo: {str(e)}')



@low.route('/processFile', methods=['POST'])
def processFile():
    url_folder = request.form.get('url_folder')
    functionApp = request.form.get('functionApp')

    # Validar que el parámetro URL existe
    if not url_folder:
        return responseBuilder.error('No se especificó una URL válida')

    try:
        data = {}

        # Procesar según el tipo de función
        if functionApp == "low":
            # Procesar archivos Acepta
            acepta_response = model.createFileAcepta(url_folder).get_json()
            if not acepta_response['success']:
                return responseBuilder.error(acepta_response['message'])

            # Preparar datos para Acepta
            data = {
                'folder_path': acepta_response['data']['folder_path'], 
                'message': acepta_response['message']
            }
            return responseBuilder.success('Archivos Acepta creados correctamente.', data)

        elif functionApp == "validate":
            print("opcion escoggida validate")
            # Procesar archivos Sunat
            sunat_response = model.createFileSunat(url_folder).get_json()
            if not sunat_response['success']:
                return responseBuilder.error(sunat_response['message'])

            # Preparar datos para Sunat
            data = {
                'folder_path': sunat_response['data']['folder_path'],
                'message': sunat_response['message']
            }
            return responseBuilder.success('Archivo SUNAT creado correctamente.', data)
        else:
            # Si el valor de functionApp no es válido
            return responseBuilder.error('El valor de functionApp no es válido. Solo se permiten "low" o "validate".')

    except Exception as e:
        return responseBuilder.error(f'Ocurrió un error al procesar los archivos: {str(e)}')





@low.route('/downloadFiles', methods=['POST'])
def downloadFiles():
    url_folder = request.form.get('url_folder')

    if not url_folder:
        return responseBuilder.error('No se especificó una URL válida')

    try:
        # Descargar archivos ZIP
        return model.downloadFiles(url_folder)

    except Exception as e:
        return responseBuilder.error(f'Ocurrió un error al descargar los archivos: {str(e)}')