import json
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

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
            return jsonify({"message": "password should not contain spaces"}), 400


        # Check if users.json exists, create it if not
        if not os.path.isfile("users.json"):
            with open("users.json", "w") as file:
                json.dump({"users": []}, file, indent=4)
        
        # Load JSON data from a file
        with open("users.json", "r") as file:
            data = json.load(file)

        # Extract the list of users
        users = data.get("users", [])

        # Check if the username already exists
        if any(user["username"] == username for user in users):
             return jsonify({"message": "Username is taken"})

        else:
            print("Username is available. You can add it.")
            # Add the new user
            users.append({"username": username, "password": password})

            # Save the updated data back to the JSON file
            with open("users.json", "w") as file:
                json.dump({"users": users}, file, indent=4)

        return jsonify({"message": "User registered successfully"})
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"message": f"An error occurred: {e}"}), 500

@app.route('/')
def clock():
    return render_template('url.html')

@app.route('/<filename>')
def file(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
