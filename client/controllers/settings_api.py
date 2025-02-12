import threading
from http import HTTPStatus

from flask import Flask, render_template, request, jsonify, session

from auths.session_handler import SessionHandler
from globals.env_variables_handler import EnvVariablesHandler
from services.settings_service import SettingsService


class SettingsApi:

    # static variables
    _instance = None
    _lock = threading.Lock()

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

        @app.route('/settingsPage')
        def settingsPage():
            return render_template(
                'settingsPage.html',
                BACKEND_URL=EnvVariablesHandler.get_instance().get_backend_url())