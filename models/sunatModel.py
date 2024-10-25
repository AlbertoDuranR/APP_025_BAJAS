import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from utils.statusSunatUtil import estado_cp_map, estado_ruc_map, cond_domi_ruc_map
import time
import os
import json
import pandas as pd
import concurrent.futures
from connection.cookie import getTokenDB


class SunatValidator:
    def __init__(self):
        self.url = "https://ww1.sunat.gob.pe/ol-ti-itconsultaunificada/consultaUnificada/importarFromTXT"
        self.cookie = getTokenDB()
        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "es-ES,es;q=0.9,en;q=0.8",
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        self.cookies = {
            'f5_cspm': '1234',
            'ITCONSULTAUNIFICADASESSION': self.cookie
        }

    def actualizarCookie(self):
        """Obtiene un nuevo token desde la base de datos y actualiza la cookie."""
        self.cookie = getTokenDB()  # Obtener nuevo token de la base de datos
        self.cookies['ITCONSULTAUNIFICADASESSION'] = self.cookie
        print("Cookie actualizada exitosamente.")


    def leerArchivo(self, file_path: str) -> bytes:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo '{file_path}' no se encontró.")
        
        with open(file_path, "rb") as file:
            file_content = file.read()
            if not file_content:
                raise ValueError("El archivo está vacío o no es accesible.")
        
        return file_content

    def prepararMultipart(self, file_path: str) -> MultipartEncoder:
        file_content = self.leerArchivo(file_path)
        multipart_data = MultipartEncoder(
            fields={"txtarchivo": (file_path, file_content, "text/plain")}
        )
        return multipart_data

    def enviarSolicitud(self, multipart_data: MultipartEncoder) -> dict:
        """Envía la solicitud a SUNAT y maneja el error 401 con actualización de token."""
        self.headers['Content-Type'] = multipart_data.content_type
        response = requests.post(self.url, headers=self.headers, data=multipart_data, cookies=self.cookies)

        if response.status_code == 401:  # Si el token ha expirado o hay problemas de credenciales
            print("Token expirado o inválido. Obteniendo un nuevo token...")
            self.actualizarCookie()  # Actualizar la cookie con el nuevo token
            response = requests.post(self.url, headers=self.headers, data=multipart_data, cookies=self.cookies)

        try:
            return response.json()
        except ValueError:
            raise ValueError(f"Error en la respuesta, no es JSON válido: {response.text}")


    def jsonADataframe(self, json_data):
        processed_data = []
        
        for item in json_data:
            if 'observaciones' in item and isinstance(item['observaciones'], list):
                item['observaciones'] = ', '.join(item['observaciones'])
            else:
                item['observaciones'] = ''

            item['estadoCp'] = estado_cp_map.get(item.get('estadoCp', ''), 'DESCONOCIDO')
            item['estadoRuc'] = estado_ruc_map.get(item.get('estadoRuc', ''), 'DESCONOCIDO')
            item['condDomiRuc'] = cond_domi_ruc_map.get(item.get('condDomiRuc', ''), 'DESCONOCIDO')

            processed_data.append(item)
        
        df = pd.DataFrame(processed_data)
        return df

    def peticiones(self, ruta):
        multipart_data = self.prepararMultipart(ruta)
        respuesta = self.enviarSolicitud(multipart_data)
               
        if isinstance(respuesta, str):
            respuesta_json = json.loads(respuesta)
            # print(respuesta_json)
            if respuesta_json.get('rpta') == 1:
                data = respuesta_json['lista']
                df = self.jsonADataframe(data)
                return df  # Retorna el DataFrame
            else:
                print("Error en la respuesta")
                return None  # Error en la respuesta
        else:
            print("Error en la respuesta principal")
            return None  # Error en la respuesta principal

    def procesarArchivo(self, file_path, max_intentos=10):
        intentos = 0
        exito = False
        while intentos < max_intentos and not exito:
            print(f"Procesando archivo: {file_path}, intento {intentos + 1}")
            try:
                df = self.peticiones(file_path)
                if df is not None:
                    print(f"Archivo {file_path} procesado con éxito en el intento {intentos + 1}")
                    return df  # Devuelve el DataFrame si tiene éxito
                else:
                    raise Exception("Error en la respuesta de la plataforma")
            except Exception as e:
                intentos += 1
                print(f"Error procesando el archivo {file_path}. Intento {intentos}/{max_intentos}. Error: {e}")
                if intentos < max_intentos:
                    time.sleep(2)  # Espera antes de reintentar
                else:
                    print(f"Falló al procesar el archivo {file_path} después de {max_intentos} intentos.")
                    return None  # Retorna None si falló

    def procesarArchivos(self, folder_path: str, max_workers=5, max_intentos=10):
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"La carpeta '{folder_path}' no se encontró.")
        
        archivos_encontrados = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        # Ejecutar en paralelo usando ThreadPoolExecutor
        lista_dataframes = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Ejecutar la función `procesarArchivo` en paralelo para cada archivo
            futuros = [executor.submit(self.procesarArchivo, file_path, max_intentos) for file_path in archivos_encontrados]
            
            for futuro in concurrent.futures.as_completed(futuros):
                try:
                    resultado = futuro.result()
                    if resultado is not None:
                        lista_dataframes.append(resultado)  # Agregar DataFrame a la lista si tuvo éxito
                except Exception as e:
                    print(f"Error procesando un archivo: {e}")

        # Concatenar todos los DataFrames en uno solo
        if lista_dataframes:
            df_final = pd.concat(lista_dataframes, ignore_index=True)
            print("Todos los DataFrames unidos en uno solo:")
            return df_final
        else:
            print("No se generaron DataFrames.")
            return None