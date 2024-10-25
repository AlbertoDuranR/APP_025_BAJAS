import psycopg2

def getTokenDB():
    """Obtiene el valor de la cookie 'ITCONSULTAUNIFICADASESSION' desde la base de datos."""

    # Configuración de conexión a la base de datos
    conn_params = {
        'host': "40.86.9.189",
        'dbname': "RhDB2",
        'user': "sqladmin",
        'password': "Slayer20fer..",
        'port': "5433"
    }

    select_query = """
        SELECT cookie FROM app_bajas 
        ORDER BY fecha DESC 
        LIMIT 1;
    """
    
    try:
        # Conectar a la base de datos y realizar la consulta
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                # Ejecutar la consulta SELECT
                cursor.execute(select_query)
                
                # Obtener el resultado
                result = cursor.fetchone()
                if result:
                    token = result[0]
                    print("Token obtenido exitosamente de la base de datos:", token)
                    return token
                else:
                    print("No se encontró ningún token en la base de datos.")
                    return None
    except Exception as e:
        print(f"Ocurrió un error al obtener el token de la base de datos: {e}")
        return None

# Ejemplo de uso
# if __name__ == "__main__":
#     token = get_token()
#     if token:
#         print("Token actual:", token)
#     else:
#         print("No se pudo obtener el token.")
