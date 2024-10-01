import os
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
            txtFolder = os.path.join(newFolderPath, 'txt')
            os.makedirs(txtFolder, exist_ok=True)
        
        except Exception as e:
            print(f"Error al crear los directorios: {str(e)}")
        
        # Retorna la ruta de la carpeta principal
        return newFolderPath
    

# Testear
# ap = getUploadFolder()
# resp = ap.createDirectory()
# print(resp)
