from flask import Flask, redirect
from flask_cors import CORS

# importamos las rutas
from routes.lowRoute import low

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# registramos los Blueprints
app.register_blueprint(low, url_prefix='/low')

# Definir una ruta de redireccionamiento por defecto a '/low'
@app.route('/')
def default():
    return redirect('/low')

if __name__ == '__main__':
    app.run(port=8007,  debug=True)