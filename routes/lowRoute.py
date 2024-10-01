from flask import Blueprint, jsonify, render_template, request, send_file


low = Blueprint('low', __name__)

# importar plantilla html
@low.route('/', methods=['GET'])
def process_index():
    return render_template('low.html')