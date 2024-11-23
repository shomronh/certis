import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from UserRepository import UserRepository


# app = Flask(__name__)
# app.secret_key = "IxfTJGSMIs{um"

class LoginApi:

    def initRoutes(self, app: Flask):

        # rest apis
        @app.route('/login', methods=['POST'])
        def login():

            data = request.get_json()

            if not data:
                return jsonify({"message": "Please enter credentials"}), 400

            username = data.get('username')
            password = data.get('password')

            user = UserRepository()
            answer = user.login(username, password)
            #Checks the answer and returns the status code with relevant response
            if answer == "Login successful":
                return jsonify({"message": answer}), 200
            elif answer == "Please register before trying to log in":
                return jsonify({"message": answer}), 404  # Missing file, send 404 status
            else:
                return jsonify({"message": answer}), 401  # Invalid credentials

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
