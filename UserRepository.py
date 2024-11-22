import os
import json
from flask import jsonify


class UserRepository:

    def check_if_file_exist(self):
        # Check if users.json exists, create it if not, create it
        if not os.path.isfile("users.json"):
            with open("users.json", "w") as file:
                json.dump({"credentials": []}, file, indent=4)

    def register(self, username, password):
        with open("users.json", "r") as file:
            users = json.load(file)

        # Extract the credentials list
        credentials = users.get("credentials", [])

        # Check if the username already exists
        if any(user["username"] == username for user in credentials):
            return "Username is taken"
        else:
            print("Username is available. You can add it.")
            # Add the new user
            credentials.append({"username": username, "password": password})

            # Save the updated data back to the JSON file
            users["credentials"] = credentials
            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)

        return "User registered successfully"
