from flask import jsonify

class responseBuilder:
    
    @staticmethod
    def build(success, message, data=None):
        """
        Construir una respuesta JSON predeterminada.
        :param success: Indica si la respuesta es exitosa o no (True/False)
        :param message: Mensaje de la respuesta
        :param data: Datos adicionales (None por defecto)
        :return: Respuesta JSON para Flask
        """
        response = {
            'success': success,
            'message': message,
            'data': data
        }
        return jsonify(response)

    @staticmethod
    def success(message, data=None):
        """
        Respuesta de éxito predeterminada.
        :param message: Mensaje de éxito
        :param data: Datos adicionales (None por defecto)
        :return: Respuesta JSON exitosa
        """
        return responseBuilder.build(True, message, data)

    @staticmethod
    def error(message, data=None):
        """
        Respuesta de error predeterminada.
        :param message: Mensaje de error
        :param data: Datos adicionales (None por defecto)
        :return: Respuesta JSON con error
        """
        return responseBuilder.build(False, message, data)
