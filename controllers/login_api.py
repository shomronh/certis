from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from http import HTTPStatus
from repositories.users_repository import UsersRepository
from services.login_service import LoginService


class LoginApi:

    def __init__(self):
        self._loginService = LoginService()

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

            s

        # Visual Routes
        @app.route('/dashboardPage')
        def dashboard():
            if "username" in session:
                username = session["username"]
                return render_template('dashboardPage.html', username=username)
            else:
                return redirect(url_for("loginPage"))

        @app.route('/loginPage')
        def loginPage():
            return render_template('loginPage.html')
