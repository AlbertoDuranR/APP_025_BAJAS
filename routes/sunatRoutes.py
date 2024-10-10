from flask import Blueprint, render_template, request, send_file
from utils.responseBuilder import responseBuilder
from models.sunatModel import SunatValidator
import json, os
from datetime import datetime 
import pytz


sunat = Blueprint('sunat', __name__)

model = SunatValidator()

# Ruta para la plantilla HTML
@sunat.route('/', methods=['GET'])
def process_index():
    return render_template('cookie.html')


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
    

@sunat.route('/updateToken', methods=['POST'])
def updateToken():
    token = request.form.get('cookie')
    
    if not token:
        return responseBuilder.error('No se especificó un token válido')

    try:
        # Definir la ruta del archivo cookie.json
        cookie_file_path = os.path.join('token', 'cookie.json')

        # Leer el archivo JSON actual
        with open(cookie_file_path, 'r') as file:
            cookie_data = json.load(file)

        # Obtener la zona horaria de Perú
        peru_tz = pytz.timezone('America/Lima')
        
        # Obtener la fecha y hora actual en la zona horaria de Perú
        peru_time = datetime.now(peru_tz).strftime('%Y-%m-%dT%H:%M:%S')

        # Actualizar el campo "cookie" y "dateTime"
        cookie_data['cookie'] = token
        cookie_data['dateTime'] = peru_time

        # Guardar los cambios en el archivo JSON
        with open(cookie_file_path, 'w') as file:
            json.dump(cookie_data, file, indent=4)

        return responseBuilder.success('Token actualizado correctamente')

    except Exception as e:
        return responseBuilder.error(f"Ocurrió un error al actualizar el token: {str(e)}")
    


@sunat.route('/getToken', methods=['GET'])
def getToken():
    try:
        # Definir la ruta del archivo cookie.json
        cookie_file_path = os.path.join('token', 'cookie.json')

        # Leer el archivo JSON actual
        with open(cookie_file_path, 'r') as file:
            cookie_data = json.load(file)

        # Devolver la información de la cookie
        return responseBuilder.success("cookie obtenido correctamente",cookie_data)

    except Exception as e:
        return responseBuilder.error(f"Ocurrió un error al obtener el token: {str(e)}")