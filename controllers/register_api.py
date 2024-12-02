from http import HTTPStatus

from flask import Flask, render_template, request, jsonify, session

from env_variable_service import EnvVariablesService
from services.register_service import RegisterService


class RegisterApi:

    def __init__(self):
        self._registerService = RegisterService.get_instance()

    def initRoutes(self, app: Flask):

        @app.route('/register', methods=['POST'])
        def data_insert():
            try:
                data = request.get_json()

                if not data:
                    return jsonify({"message": "Please enter credentials"}), HTTPStatus.UNAUTHORIZED

                print(f"Received data: {data}")

                if not data:
                    return jsonify({"message": "Invalid JSON data"}), 400

                username = data.get('username')
                password = data.get('password')

                message, is_ok = self._registerService.register(username, password)

                if is_ok:
                    return jsonify({"message": message}), HTTPStatus.OK
                else:
                    return jsonify({"message": message}), HTTPStatus.UNAUTHORIZED


            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

        @app.route('/registerPage')
        def RegisterPage():
            return render_template(
                'registerPage.html',
                BACKEND_URL=EnvVariablesService.get_instance().get_backend_url())
