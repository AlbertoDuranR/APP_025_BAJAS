from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import time
import glob
from utils.responseBuilder import responseBuilder

class aceptaModel:
    def __init__(self,):
        self.driver = None
        self.selenium_grid_url = "http://40.86.9.189:4444"

    # Función para iniciar el navegador usando Selenium Grid
    def iniciar_navegador(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        # Configuramos el navegador para conectarse al Selenium Grid
        self.driver = webdriver.Remote(
            command_executor=self.selenium_grid_url,
            options=chrome_options
        )

    # Función para iniciar sesión
    def iniciar_sesion(self):
        self.driver.get("https://escritorio.acepta.pe")
        self.driver.find_element("id", "loginrut").send_keys("fernando.colque@terranovatrading.com.pe")
        self.driver.find_element("name", "LoginForm[password]").send_keys("19884213")
        self.driver.find_element("xpath", "//input[@value='Ingresar']").click()

    # Función para navegar al menú de Comunicación de Baja
    def navegar_menu_baja(self):
        menu_baja = '/html/body/div[8]/div[1]/aside/ul/li[8]/a/span[1]'
        self.driver.find_element("xpath", menu_baja).click()

        submenu_generar = '/html/body/div[8]/div[1]/aside/ul/li[8]/ul/li[2]/a'
        self.driver.find_element("xpath", submenu_generar).click()

    # Función para subir el archivo de Baja
    def subir_archivo_baja(self, filename):
        time.sleep(5)
        page_subir_baja = '/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div/div/div/ul/li[2]'
        wait = WebDriverWait(self.driver, 60)
        wait.until(ec.visibility_of_element_located((By.XPATH, page_subir_baja)))
        self.driver.find_element("xpath", page_subir_baja).click()

        time.sleep(5)
        absolute_path = os.path.abspath(filename)
        select = '/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div[1]/form/div[1]/input'
        wait.until(ec.visibility_of_element_located((By.XPATH, select)))
        self.driver.find_element("xpath", select).send_keys(absolute_path)

    # Función para dar de baja el archivo procesado
    def dar_baja(self):
        baja_xpath = '/html/body/div[8]/div[1]/section/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div[4]/form/div[1]/input'
        wait = WebDriverWait(self.driver, 60).until(ec.visibility_of_element_located((By.XPATH, baja_xpath)))
        self.driver.find_element("xpath", baja_xpath).click()

        time.sleep(10)
        alerta_baja = self.esperar_alerta()
        if alerta_baja == "Resumen generado correctamente":
            return f"Alerta: {alerta_baja}"
        return ""

    # Función para esperar la alerta y retornar el texto de la alerta
    def esperar_alerta(self):
        try:
            wait = WebDriverWait(self.driver, 60)
            alert = wait.until(ec.alert_is_present())
            alert_text = alert.text
            alert.accept()
            return alert_text
        except:
            return None

    # Función para procesar el archivo en varios intentos
    def procesar_archivo(self, filename, intentos):
        log_mensajes = f"Archivo: {os.path.basename(filename)}\n"

        for intento in range(intentos):
            print(f"Reintento {intento + 1}")
            self.subir_archivo_baja(filename)
            alert_text = self.esperar_alerta()

            if alert_text and "procesado correctamente" in alert_text:
                log_mensajes += f"{os.path.basename(filename)} procesado con éxito.\n"
                return log_mensajes, True
            else:
                log_mensajes += f"Alerta: {alert_text}\nReintento {intento + 1}\n"

        log_mensajes += f"Error después de {intentos} reintentos\n\n"
        return log_mensajes, False

    # Función principal que coordina el flujo y procesa todos los archivos CSV
    def rpa_acepta_todos(self, archivos_csv):
        log_final = ""

        try:
            self.iniciar_navegador()
            self.iniciar_sesion()
            self.navegar_menu_baja()

            # Procesar cada archivo CSV
            for archivo in archivos_csv:
                log_mensajes = f"Procesando archivo: {os.path.basename(archivo)}\n"
                log_mensajes, exito = self.procesar_archivo(archivo, 3)

                log_final += log_mensajes

                if exito:
                    log_final += self.dar_baja() + "\n"
                else:
                    log_final += f"Falló el procesamiento de {os.path.basename(archivo)} después de 3 intentos.\n\n"

            # Si todo salió bien, devolver log_final como respuesta exitosa
            return responseBuilder.success(log_final)

        except Exception as e:
            # En caso de excepción, devolver log_final con el error
            log_final += f"Error: {str(e)}\n"
            return responseBuilder.error(log_final)

        finally:
            self.driver.quit()
