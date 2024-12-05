import threading
from http import HTTPStatus

from flask import Flask, render_template, request, jsonify

from env_variable_service import EnvVariablesService
from services.logs_service import LogsService
from services.register_service import RegisterService


class RegisterApi:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables

    @classmethod
    def get_instance(cls, app: Flask):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.initRoutes(app)
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def initRoutes(self, app: Flask):

        logger = LogsService.get_instance()

        self._registerService = RegisterService.get_instance()

        @app.route('/register', methods=['POST'])
        def data_insert():
            try:
                data = request.get_json()

                if not data:
                    return jsonify({"message": "Please enter credentials"}), HTTPStatus.UNAUTHORIZED

                logger.log(f"Received data: {data}")

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
