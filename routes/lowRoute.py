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

    if not file:
        return responseBuilder.error('No se cargó ningún archivo')

    if not period:
        return responseBuilder.error('No se especificó un período')

    try:
        # Crear la carpeta para almacenar el archivo
        upload_folder = urlFile.getUploadFolder()
        
        # Guardar el archivo subido en la carpeta creada
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Limpiar el archivo para Acepta y filtrar por el período
        return model.fileCleanup(upload_folder, file_path, period)
       
    except Exception as e:
        # Manejo de errores durante el proceso de carga de archivos
        return responseBuilder.error(f'Ocurrió un error al procesar el archivo: {str(e)}')



@low.route('/processFile', methods=['POST'])
def processFile():
    
    url_folder = request.form.get('url_folder')

    if not url_folder:
        return responseBuilder.error('No se especificó una URL válida')
    
    try:
        # Procesar archivos Acepta
        acepta_response = model.createFileAcepta(url_folder).get_json()
        if not acepta_response['success']:
            return responseBuilder.error(acepta_response['message'])

        # Procesar archivos Sunat
        sunat_response = model.createFileSunat(url_folder).get_json()
        if not sunat_response['success']:
            return responseBuilder.error(sunat_response['message'])

        # Combinar respuestas de éxito usando diccionarios
        combined_data = {
            'acepta_response': {
                'folder_path': acepta_response['data']['folder_path'], 
                'message': acepta_response['message']
            },
            'sunat_response': {
                'folder_path': sunat_response['data']['folder_path'], 
                'message': sunat_response['message']
            }
        }

        return responseBuilder.success('Archivos Acepta y SUNAT creados correctamente.', combined_data)

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