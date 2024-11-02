import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import time

class SunatValidator:
    def __init__(self):
        self.url = "https://ww1.sunat.gob.pe/ol-ti-itconsultaunificada/consultaUnificada/importarFromTXT"
        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "es-ES,es;q=0.9,en;q=0.8",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Referer": "https://ww1.sunat.gob.pe/ol-ti-itconsultaunificada/consultaUnificada/consulta",
            "Referer-Policy": "strict-origin-when-cross-origin"
        }
        self.cookies = {
            "f5avraaaaaaaaaaaaaaaa_session_": "GHOAABOOBGLBEEILALOLIOBLAPJFDABEJNJDALLNNIBILNIEOKANIJEOJGGPLHMCJJEDEHAMGCIJKGCDFCMAJLOCJEGBMJOEDJJDEOOBPPFHKCEGNKEICLNIHEONMAFA",
            "f5_cspm": "1234",
            "ITCONSULTAUNIFICADASESSION": "sdHtevolxTvMzN7II83FDyethbkbBd_4NviACxJCrbTF3Byep_0JAK2eGu2DgdDpDurRTrTypf41ous_eVlnl7ecmRD93dIsAfljR_bhq2uEk2KAfcEh6MR2_VYjkVmxE8HIOBKGJwL8URg5GSqoCunBymly99DxjUiOVnHjLSntDPunWyJuZ1Z4ezZvvRosDUVAZokTWoMkZ4rMJDkPdUHcnu4t4yLipAoeX_AtBp4PT-l3_mxB6HHzXW3EoZs1"
        }

    def enviarSolicitud(self, file_path: str):
        # Preparar el archivo en formato multipart/form-data
        multipart_data = MultipartEncoder(
            fields={
                "txtarchivo": (file_path, open(file_path, "rb"), "text/plain")
            }
        )

        # Añadir el tipo de contenido a los encabezados
        self.headers["Content-Type"] = multipart_data.content_type

        # Intentar la solicitud
        for intento in range(3):  # Intentos de reintento si falla
            try:
                print(f"Enviando solicitud a SUNAT (Intento {intento + 1})...")
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    data=multipart_data,
                    cookies=self.cookies,
                    timeout=60
                )

                # Verificar si el servidor rechazó la solicitud
                if response.status_code == 401:
                    print("Error 401: Token expirado o inválido. Intentando nuevamente...")
                    time.sleep(5)  # Pausa antes de reintentar
                    continue

                # Revisar si la respuesta es HTML (indica un rechazo)
                if "<html>" in response.text:
                    print("Error: Solicitud rechazada por el servidor.")
                    print("Respuesta HTML recibida:", response.text)
                    return None

                # Si todo está bien, retorna la respuesta en JSON
                return response.json()

            except requests.Timeout:
                print("Error: Tiempo de espera excedido en la solicitud a SUNAT.")
                time.sleep(5)  # Pausa antes de reintentar

        print("Error: No se pudo completar la solicitud después de varios intentos.")
        return None

# Ejemplo de uso
validador = SunatValidator()
respuesta = validador.enviarSolicitud("sunat_1.txt")
if respuesta:
    print("Respuesta JSON:", respuesta)
else:
    print("Error al obtener la respuesta de SUNAT.")
