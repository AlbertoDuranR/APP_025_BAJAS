from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import time
from utils.responseBuilder import responseBuilder

class aceptaModel:
    def __init__(self):
        self.driver = None
        self.selenium_grid_url = "http://40.86.9.189:4444"

    def iniciar_navegador(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Remote(
            command_executor=self.selenium_grid_url,
            options=chrome_options
        )

    def iniciar_sesion(self):
        self.driver.get("https://escritorio.acepta.pe")
        self.driver.find_element(By.ID, "loginrut").send_keys("fernando.colque@terranovatrading.com.pe")
        self.driver.find_element(By.NAME, "LoginForm[password]").send_keys("54740293")
        self.driver.find_element(By.XPATH, "//input[@value='Ingresar']").click()

    def navegar_menu_baja(self):
        menu_baja = '/html/body/div[8]/div[1]/aside/ul/li[8]/a/span[1]'
        submenu_generar = '/html/body/div[8]/div[1]/aside/ul/li[8]/ul/li[2]/a'
        self.driver.find_element(By.XPATH, menu_baja).click()
        self.driver.find_element(By.XPATH, submenu_generar).click()

    def subir_archivo_baja(self, filename):
        WebDriverWait(self.driver, 60).until(
            ec.visibility_of_element_located((By.XPATH, '/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div/div/div/ul/li[2]'))
        ).click()
        time.sleep(5)
        absolute_path = os.path.abspath(filename)
        select = '/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div[1]/form/div[1]/input'
        WebDriverWait(self.driver, 60).until(ec.visibility_of_element_located((By.XPATH, select)))
        self.driver.find_element(By.XPATH, select).send_keys(absolute_path)

    def dar_baja(self):
        baja_xpath = '/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div[4]/form/div[1]/input'
        WebDriverWait(self.driver, 60).until(ec.visibility_of_element_located((By.XPATH, baja_xpath))).click()
        time.sleep(10)
        return self.esperar_alerta()

    def esperar_alerta(self):
        try:
            alert = WebDriverWait(self.driver, 60).until(ec.alert_is_present())
            alert_text = alert.text
            alert.accept()
            return alert_text
        except:
            return None

    def procesar_archivo(self, filename, intentos):
        respuestas = []
        for intento in range(intentos):
            self.subir_archivo_baja(filename)
            alert_text = self.esperar_alerta()
            if alert_text:
                respuestas.append(f"Intento {intento + 1}: {alert_text}")
                if "procesado correctamente" in alert_text:
                    return respuestas, True
            else:
                respuestas.append(f"Intento {intento + 1}: Fallo sin alerta.")
            time.sleep(5)  # Breve pausa entre intentos

        respuestas.append("Error después de varios intentos fallidos.")
        return respuestas, False

    def rpa_acepta_todos(self, archivos_csv):
        resultados = []
        logs = []

        try:
            self.iniciar_navegador()
            self.iniciar_sesion()
            self.navegar_menu_baja()

            for archivo in archivos_csv:
                archivo_nombre = os.path.basename(archivo)
                respuestas, exito = self.procesar_archivo(archivo, 1)

                resultado = {
                    "archivo": archivo_nombre,
                    "respuestas": respuestas
                }

                if exito:
                    baja_mensaje = self.dar_baja()
                    if baja_mensaje:
                        resultado["respuestas"].append(baja_mensaje)

                resultados.append(resultado)

            return responseBuilder.success("Proceso completado", {"resultados": resultados, "logs": logs})

        except Exception as e:
            logs.append({
                "tipo_error": "Excepción",
                "mensaje_error": str(e)
            })
            return responseBuilder.error("Ocurrió un error durante el procesamiento", {"resultados": resultados, "logs": logs})

        finally:
            if self.driver:
                self.driver.quit()
