import threading
from http import HTTPStatus

from flask import Flask, request, jsonify, session
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from services.login_service import LoginService
from services.register_service import RegisterService


class GoogleLoginApi:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables

    @classmethod
    def get_instance(cls, app: Flask):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__init(app)
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self, app: Flask):

        self.__loginService = LoginService.get_instance()
        self.__registerService = RegisterService.get_instance()

        @app.route('/google-auth', methods=['POST'])
        def google_auth():
            # Get the ID token from the frontend
            id_token_received = request.json.get('id_token')

            # Verify the token using Google's public keys
            try:
                # Your Google Client ID from the Developer Console
                client_id = '646869605585-0i2ljqvpddcj40m7vnho8818mft60rta.apps.googleusercontent.com'

                # Verify the ID token and decode the user information
                id_info = id_token.verify_oauth2_token(id_token_received, Request(), client_id)

                username = id_info['email']
                password = id_info['aud']

                # id_info will contain user info such as email, name, etc.
                # return jsonify(id_info), HTTPStatus.OK  # Return user info or any other response

                message, is_ok = self.__loginService.login(username, password)

                if not is_ok:
                    message, is_ok = self.__registerService.register(username, password)

                    if not is_ok:
                        return jsonify({"message": message}), HTTPStatus.UNAUTHORIZED

                session['username'] = username
                return jsonify({"message": message, "username": username}), HTTPStatus.OK

            except ValueError:
                return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

        



