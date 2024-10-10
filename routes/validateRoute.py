from flask import Blueprint, render_template, request, send_file
from models.lowModel import LowModel
from utils.urlFileUtils import UrlFile
from utils.responseBuilder import responseBuilder
import os

validate = Blueprint('validate', __name__)

# Inicializar el objeto urlFile y LowModel
urlFile = UrlFile()
model = LowModel()

# Ruta para la plantilla HTML
@validate.route('/', methods=['GET'])
def process_index():
    return render_template('validate.html')



@validate.route('/processFile', methods=['POST'])
def processFile():
    
    url_folder = request.form.get('url_folder')

    if not url_folder:
        return responseBuilder.error('No se especificó una URL válida')
    
    try:

        # Procesar archivos Sunat
        sunat_response = model.createFileSunat(url_folder).get_json()
        if not sunat_response['success']:
            return responseBuilder.error(sunat_response['message'])

        # Combinar respuestas de éxito usando diccionarios
        combined_data = {
            'sunat_response': {
                'folder_path': sunat_response['data']['folder_path'], 
                'message': sunat_response['message']
            }
        }

        return responseBuilder.success('Archivos Acepta y SUNAT creados correctamente.', combined_data)

    except Exception as e:
        return responseBuilder.error(f'Ocurrió un error al procesar los archivos: {str(e)}')



