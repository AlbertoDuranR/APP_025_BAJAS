import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from utils.statusSunatUtil import estado_cp_map, estado_ruc_map, cond_domi_ruc_map
import time
import os
import json
import pandas as pd
import concurrent.futures
from connection.cookie import getTokenDB
from datetime import datetime

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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        self.cookies = {
            'f5_cspm': '1234',
            'ITCONSULTAUNIFICADASESSION': self.cookie
        }

    def actualizarCookie(self):
        """Obtiene un nuevo token desde la base de datos y actualiza la cookie."""
        self.cookie = getTokenDB()
        self.cookies['ITCONSULTAUNIFICADASESSION'] = self.cookie

    def leerArchivo(self, file_path: str) -> bytes:
        if not os.path.exists(file_path):
            print(f"Error: Archivo no encontrado: {file_path}")
            raise FileNotFoundError(f"El archivo '{file_path}' no se encontró.")
        
        with open(file_path, "rb") as file:
            file_content = file.read()
            if not file_content:
                print(f"Error: El archivo está vacío o no es accesible: {file_path}")
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
        try:
            print("Enviando solicitud a SUNAT...")
            response = requests.post(self.url, headers=self.headers, data=multipart_data, cookies=self.cookies, timeout=60)

            if response.status_code == 401:
                print("Error: Token expirado o inválido. Actualizando token.")
                self.actualizarCookie()
                response = requests.post(self.url, headers=self.headers, data=multipart_data, cookies=self.cookies, timeout=60)
            return response.json()
        except requests.Timeout:
            print("Error: Tiempo de espera excedido en la solicitud a SUNAT.")
            raise TimeoutError("Tiempo de espera excedido en la solicitud a SUNAT.")
        except ValueError:
            print(f"Error: Respuesta no es JSON válido: {response.text}")
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
            if respuesta_json.get('rpta') == 1:
                data = respuesta_json['lista']
                df = self.jsonADataframe(data)
                return df
            else:
                print("Error: Respuesta JSON recibida es incorrecta")
                return None
        else:
            print("Error: Respuesta principal es incorrecta")
            return None

    def procesarArchivo(self, file_path, max_intentos=10):
        intentos = 0
        while intentos < max_intentos:
            intentos += 1
            try:
                df = self.peticiones(file_path)
                if df is not None:
                    print(f"Intento {intentos}: procesamiento exitoso")
                    return df
                else:
                    raise Exception("Error en la respuesta de la plataforma")
            except Exception as e:
                print(f"Intento {intentos}: error - {e}")
                time.sleep(8)
                
        print(f"Falló el procesamiento del archivo '{file_path}' después de {max_intentos} intentos.")
        return None

    def procesarArchivos(self, folder_path: str, max_workers=10, max_intentos=5):
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"La carpeta '{folder_path}' no se encontró.")
        
        archivos_encontrados = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        lista_dataframes = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futuros = [executor.submit(self.procesarArchivo, file_path, max_intentos) for file_path in archivos_encontrados]
            
            for futuro in concurrent.futures.as_completed(futuros):
                try:
                    resultado = futuro.result()
                    if resultado is not None:
                        lista_dataframes.append(resultado)
                except Exception as e:
                    print(f"Error procesando un archivo en paralelo: {e}")

        if lista_dataframes:
            df_final = pd.concat(lista_dataframes, ignore_index=True)
            return df_final
        else:
            print("Error: No se generaron DataFrames.")
            return None
