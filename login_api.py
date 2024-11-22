import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# app = Flask(__name__)
# app.secret_key = "IxfTJGSMIs{um"

class LoginApi:

    def initRoutes(self, app: Flask):

        # rest apis
        @app.route('/login', methods=['POST'])
        def login():
            try:
                # Open and read the JSON file
                with open('users.json', 'r') as file:
                    user_data = json.load(file)

                data = request.get_json()

                if not data:
                    return jsonify({"message": "Please enter credentials"}), 400

                username = data.get('username')
                password = data.get('password')

                # Check credentials
                for user in user_data['credentials']:
                    if username == user['username'] and password == user['password']:
                        session["username"] = username  # Store username in session
                        return jsonify({"message": "Login successful"}), 200

                # If credentials do not match
                return jsonify({"message": "Invalid credentials, please try again"}), 401

            except FileNotFoundError:
                print("File not found error.")
                return jsonify({"message": "Please register before trying to log in"}), 400
            except Exception as e:
                print(f"An error occurred: {e}")
                return jsonify({"message": f"An error occurred: {e}"}), 500

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
