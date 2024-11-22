import json
from flask import Flask, render_template, request, jsonify
import os
from UserRepository import UserRepository


class RegisterApi:

    def initRoutes(self, app: Flask):

        @app.route('/register', methods=['POST'])
        def data_insert():
            try:
                data = request.get_json()
                print(f"Received data: {data}")

                if not data:
                    return jsonify({"message": "Invalid JSON data"}), 400

                username = data.get('username')
                password = data.get('password')

                # Check for spaces in the username
                if ' ' in username:
                    return jsonify({"message": "Username should not contain spaces"}), 400
                # Check for spaces in the password
                elif ' ' in password:
                    return jsonify({"message": "Password should not contain spaces"}), 400

                # Check if users.json exists, create it if not

                user_repo = UserRepository()

                user_repo.check_if_file_exist()

                # Load JSON data from a file
                answer = user_repo.register(username, password)
                return jsonify({"message": f"{answer}"})



            except Exception as e:
                print(f"An error occurred: {e}")
                return jsonify({"message": f"An error occurred: {e}"}), 500

        @app.route('/registerPage')
        def RegisterPage():
            return render_template('registerPage.html')
