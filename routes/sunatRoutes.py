from flask import Blueprint, render_template, request, send_file
from utils.responseBuilder import responseBuilder
from models.sunatModel import SunatValidator
from utils.statusSunatUtil import estado_cp_map, estado_ruc_map, cond_domi_ruc_map

sunat = Blueprint('sunat', __name__)

model = SunatValidator()

@sunat.route('/validate', methods=['POST'])
def validate():
    folder_path = request.form.get('folder_path')

    try:
        # Procesar archivos en la ruta proporcionada
        response = model.procesarArchivos(folder_path)

        response = response.to_dict(orient='records')

        # print(response)

        if response:  # Si hay respuesta
            # Retornar la respuesta JSON correctamente
            return responseBuilder.success('Archivos validados correctamente', response)
        else:
            return responseBuilder.error("No se pudieron validar los archivos o no hay datos disponibles")

    except Exception as e:
        return responseBuilder.error(f"Ocurrió un error al procesar los archivos: {str(e)}")