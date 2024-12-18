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

    # other variables
    __session_handler: SessionHandler

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

        self.settingsService = SettingsService.get_instance()
        self.__session_handler = SessionHandler.get_instance()

        @app.route('/user/settings/scheduler', methods=['POST'])
        def setting_scheduler():

            try:
                data = request.get_json()

                if not data:
                    return jsonify({"message": "Please enter credentials"}), HTTPStatus.UNAUTHORIZED

                user_id = data.get("user_id")
                settings = data.get("settings")

                if not self.__session_handler.validate_session(session, user_id):
                    return jsonify({"message": "user need to login first"}), HTTPStatus.UNAUTHORIZED

                message, is_ok = self.settingsService.update_scheduler_settings(user_id, settings)

                if not is_ok:
                    return jsonify({"message": message}), HTTPStatus.UNAUTHORIZED

                return jsonify({"message": message}), HTTPStatus.OK

            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

        @app.route('/settingsPage')
        def settingsPage():
            if self.__session_handler.validate_session(session):
                username = self.__session_handler.get_username(session)

                return render_template(
                    'settingsPage.html',
                    username=username,
                    BACKEND_URL=EnvVariablesHandler.get_instance().get_backend_url())
            else:
                return render_template('loginPage.html')