import os
import shutil
from datetime import datetime

class UrlFile:
    
    def getUploadFolder(self):
        # Obtener la fecha y hora actual en el formato requerido
        currentTime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        
        # Ruta base del directorio 'static/uploads'
        baseDir = os.path.join('static', 'uploads')
        
        # Nombre de la nueva carpeta con la nomenclatura año_mes_dia_hora_minuto_segundo
        newFolderName = f"{currentTime}"
        
        # Ruta completa de la nueva carpeta principal
        newFolderPath = os.path.join(baseDir, newFolderName)
        
        try:
            # Crear el directorio principal si no existe
            os.makedirs(newFolderPath, exist_ok=True)
            
            # Crear subcarpeta 'acepta' dentro de la carpeta principal
            aceptaFolder = os.path.join(newFolderPath, 'acepta')
            os.makedirs(aceptaFolder, exist_ok=True)
            
            # Crear subcarpeta 'txt' dentro de la carpeta principal
            txtFolder = os.path.join(newFolderPath, 'sunat')
            os.makedirs(txtFolder, exist_ok=True)
        
        except Exception as e:
            print(f"Error al crear los directorios: {str(e)}")
        
        # Retorna la ruta de la carpeta principal
        return newFolderPath
    
    def deleteOldFolders(self):
        # Ruta base del directorio 'static/uploads'
        baseDir = os.path.join('static', 'uploads')
        
        # Obtener la fecha actual
        today = datetime.now().strftime("%Y_%m_%d")
        
        try:
            # Listar las carpetas en el directorio base
            for folder in os.listdir(baseDir):
                folderPath = os.path.join(baseDir, folder)
                
                # Verificar que sea un directorio
                if os.path.isdir(folderPath):
                    # Extraer la fecha de la carpeta (primeros 10 caracteres: año_mes_dia)
                    folderDate = folder[:10]
                    
                    # Si la fecha de la carpeta es anterior a la fecha de hoy, eliminarla
                    if folderDate < today:
                        shutil.rmtree(folderPath)
                        print(f"Carpeta eliminada: {folderPath}")
        
        except Exception as e:
            print(f"Error al eliminar carpetas: {str(e)}")
    

# Testear
# ap = getUploadFolder()
# resp = ap.deleteOldFolders()
# print(resp)
