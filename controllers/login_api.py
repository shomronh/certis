from http import HTTPStatus

from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from env_variable_service import EnvVariablesService
from services.login_service import LoginService


class LoginApi:

    def __init__(self):
        self._loginService = LoginService.get_instance()

    def initRoutes(self, app: Flask):

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

                session['username'] = username
                return jsonify({"message": message}), HTTPStatus.OK

            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

        @app.route('/logout')
        def logout():
            session.clear()
            return redirect(url_for("/"))

        # Visual Routes
        @app.route('/dashboardPage')
        def dashboard():
            if "username" in session:
                username = session["username"]
                return render_template(
                    'dashboardPage.html',
                    username=username,
                    BACKEND_URL=EnvVariablesService.get_instance().get_backend_url())
            else:
                return redirect(url_for("/"))

        @app.route('/')
        def loginPage():
            return render_template(
                'loginPage.html',
                BACKEND_URL=EnvVariablesService.get_instance().get_backend_url())



