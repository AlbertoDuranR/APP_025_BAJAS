from flask import Blueprint, render_template, request, send_file
from utils.responseBuilder import responseBuilder
from models.sunatModel import SunatValidator

sunat = Blueprint('sunat', __name__)

model = SunatValidator()

@sunat.route('/validate', methods=['POST'])
def validate():
    folder_path = request.form.get('folder_path')

    try:
        # Procesar archivos en la ruta proporcionada
        response = model.procesarArchivos(folder_path)

        # convertir a json
        response = response.to_dict(orient='records')

        if response:  # Si hay respuesta
            # Retornar la respuesta JSON correctamente
            return responseBuilder.success('Archivos validados correctamente', response)
        else:
            return responseBuilder.error("No se pudieron validar los archivos o no hay datos disponibles")

    except Exception as e:
        return responseBuilder.error(f"Ocurrió un error al procesar los archivos: {str(e)}")