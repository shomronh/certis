import threading
from http import HTTPStatus

from flask import Flask, render_template, request, jsonify, session

from services.session_manager_service import SessionManagerService
from services.settings_service import SettingsService


class SettingsApi:

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

        self.settingsService = SettingsService.get_instance()

        @app.route('/user/settings/scheduler', methods=['POST'])
        def setting_scheduler():

            try:
                data = request.get_json()

                if not data:
                    return jsonify({"message": "Please enter credentials"}), HTTPStatus.UNAUTHORIZED

                user_id = data.get("user_id")
                settings = data.get("settings")

                if not SessionManagerService.get_instance().validate_session(session, user_id):
                    return jsonify({"message": "user need to login first"}), HTTPStatus.UNAUTHORIZED

                message, is_ok = self.settingsService.update_scheduler_settings(user_id, settings)

                if not is_ok:
                    return jsonify({"message": message}), HTTPStatus.UNAUTHORIZED

                return jsonify({"message": message}), HTTPStatus.OK

            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

        @app.route('/settingsPage')
        def settingsPage():
            return render_template('settingsPage.html')