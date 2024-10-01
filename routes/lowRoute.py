from flask import Blueprint, jsonify, render_template, request, send_file
from models.lowModel import LowModel
from utils.urlFileUtils import UrlFile  # Asegúrate de que la clase esté bien nombrada
import os

low = Blueprint('low', __name__)

# Inicializar el objeto urlFile
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
        return jsonify({'success': False, 'message': 'No se cargó ningún archivo', 'data': None})


    try:
        # Crear la carpeta para almacenar el archivo
        upload_folder = urlFile.getUploadFolder()
        
        # Guardar el archivo subido en la carpeta creada
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # crear el archivo para acepta
        responseClean = model.fileCleanup(file_path, period)
        if responseClean['success'] == False:
            return responseClean
        
        # Retornar respuesta exitosa
        return jsonify({
            'success': True,
            'message': 'Archivo cargado correctamente',
            'data': {'file_path': file_path}
        })

    except Exception as e:
        # Manejo de errores durante el proceso de carga de archivos
        return jsonify({
            'success': False,
            'message': f'Ocurrió un error al procesar el archivo: {str(e)}',
            'data': None
        })
