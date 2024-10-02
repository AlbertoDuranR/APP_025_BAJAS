# Usamos una imagen base de Python con Alpine
FROM python:alpine3.16

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /home/app

# Actualizamos e instalamos las dependencias necesarias
RUN apk update && apk add --no-cache gcc g++ libpq-dev postgresql-dev

# Copiamos el archivo de requerimientos a la imagen y luego instalamos las dependencias de Python
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt && pip3 install gunicorn

# Copiamos el código de la aplicación al directorio de trabajo en el contenedor
COPY . .

# Exponemos el puerto 5000 para Flask
EXPOSE 5000

# Definimos el comando de inicio para ejecutar la aplicación usando Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--access-logfile", "-", "--error-logfile", "-"]
