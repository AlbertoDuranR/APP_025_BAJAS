from flask import Flask, redirect
from flask_cors import CORS

# importamos las rutas
from routes.lowRoute import low
from routes.validateRoute import validate
from routes.sunatRoutes import sunat
from routes.aceptaRoute import acepta

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# registramos los Blueprints
app.register_blueprint(low, url_prefix='/low')
app.register_blueprint(validate, url_prefix='/validate')
app.register_blueprint(sunat, url_prefix='/sunat')
app.register_blueprint(acepta, url_prefix='/acepta')

# Definir una ruta de redireccionamiento por defecto a '/low'
@app.route('/')
def default():
    return redirect('/low')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001,  debug=True)