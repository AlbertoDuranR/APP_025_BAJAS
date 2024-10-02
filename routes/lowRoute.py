from flask import Blueprint, render_template, request, send_file
from models.lowModel import LowModel
from utils.urlFileUtils import UrlFile
from utils.responseBuilder import responseBuilder  # Asegúrate de importar la clase correcta

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
        return model.fileCleanup(file_path, period)
       

    except Exception as e:
        # Manejo de errores durante el proceso de carga de archivos
        return responseBuilder.error(f'Ocurrió un error al procesar el archivo: {str(e)}')
