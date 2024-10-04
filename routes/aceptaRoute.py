from flask import Blueprint, request
from utils.responseBuilder import responseBuilder
from models.aceptaModel import aceptaModel
import glob
import os

# Crear el blueprint para las rutas de 'acepta'
acepta = Blueprint('acepta', __name__)

# Ruta para el bot de baja
@acepta.route('/baja', methods=['POST'])
def validate():
    try:
        # Obtener la ruta de la carpeta de archivos desde el formulario
        folder_path = request.form.get('folder_path')

        # Verificar si la carpeta existe
        if not folder_path or not os.path.exists(folder_path):
            return responseBuilder.error("No se proporcionó una carpeta válida o no existe.")

        # Obtener todos los archivos CSV en la carpeta especificada
        archivos_csv = glob.glob(os.path.join(folder_path, '*.csv'))

        # Verificar si se encontraron archivos CSV
        if not archivos_csv:
            return responseBuilder.error("No se encontraron archivos CSV en la carpeta especificada.")

        # Instanciar el modelo aceptaModel
        model = aceptaModel()

        # Llamar al método principal que procesa los archivos
        response = model.rpa_acepta_todos(archivos_csv)

        # Devolver la respuesta del modelo (éxito o error)
        return response

    except Exception as e:
        # Manejar cualquier excepción inesperada
        return responseBuilder.buildErrorResponse(f"Ocurrió un error al procesar los archivos: {str(e)}")
