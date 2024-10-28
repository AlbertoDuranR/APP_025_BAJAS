# construir
docker build -t app_bajas .

# levantar conenedor
docker run -d -p 5000:5000 --name app_bajas_container app_bajas

# ver logs
docker logs app_bajas_container

# detener contenedor
docker stop app_bajas_container

# Instalador
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt




