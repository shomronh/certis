import threading
from http import HTTPStatus

from flask import Flask, render_template, request, jsonify

from globals.env_variables_handler import EnvVariablesHandler
from logger.logs_handler import LogsHandler
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

        logger = LogsHandler.get_instance()

        @app.route('/registerPage')
        def RegisterPage():
            return render_template(
                'registerPage.html',
                BACKEND_URL=EnvVariablesHandler.get_instance().get_backend_url())
