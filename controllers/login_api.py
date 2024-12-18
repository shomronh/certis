import threading
from http import HTTPStatus

from flask import Flask, render_template, request, jsonify, session

from auths.session_handler import SessionHandler
from globals.env_variables_handler import EnvVariablesHandler
from services.login_service import LoginService


class LoginApi:

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
                cls._instance.__init(app)
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self, app: Flask):

        self._loginService = LoginService.get_instance()
        self.__session_handler = SessionHandler.get_instance()

        # rest apis
        @app.route('/login', methods=['POST'])
        def login():

            try:
                data = request.get_json()

                if not data:
                    return jsonify({"message": "Please enter credentials"}), HTTPStatus.UNAUTHORIZED

                username = data.get('username')
                password = data.get('password')

                message, is_ok = self._loginService.login(username, password)

                if not is_ok:
                    return jsonify({"message": message}), HTTPStatus.UNAUTHORIZED

                return jsonify({"message": message, "username": username}), HTTPStatus.OK

            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

        @app.route('/logout')
        def logout():
            self._loginService.logout()
            return render_template(
                'loginPage.html',
                BACKEND_URL=EnvVariablesHandler.get_instance().get_backend_url())

        # Visual Routes
        @app.route('/dashboardPage')
        def dashboard():
            if self.__session_handler.validate_session(session):
                username = self.__session_handler.get_username(session)

                return render_template(
                    'dashboardPage.html',
                    username=username,
                    BACKEND_URL=EnvVariablesHandler.get_instance().get_backend_url())
            else:
                return loginPage()

        @app.route('/')
        def loginPage():
            return render_template(
                'loginPage.html',
                BACKEND_URL=EnvVariablesHandler.get_instance().get_backend_url())

        @app.errorhandler(404)
        def page_not_found(err):
            return dashboard()

        @app.errorhandler(500)
        def internal_server_error(err):
            return ashboard()