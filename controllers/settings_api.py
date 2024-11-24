from http import HTTPStatus

from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from services.settings_service import SettingsService


class SettingsApi:

    def __init__(self):
        self.settingsService = SettingsService()

    def initRoutes(self, app: Flask):

        @app.route('/user/settings/scheduler', methods=['POST'])
        def setting_scheduler():

            try:
                if "username" not in session:
                    return jsonify({"message": "user need to login first"}), HTTPStatus.UNAUTHORIZED

                data = request.get_json()

                if not data:
                    return jsonify({"message": "Please enter credentials"}), HTTPStatus.UNAUTHORIZED

                user_id = data.get("user_id")
                settings = data.get("settings")

                message, is_ok = self.settingsService.update_scheduler_settings(user_id, settings)

                if not is_ok:
                    return jsonify({"message": message}), HTTPStatus.UNAUTHORIZED

                return jsonify({"message": message}), HTTPStatus.OK

            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

