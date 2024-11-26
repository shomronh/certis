import os
import json
from flask import jsonify


class UsersRepository:

    def __init__(self, directory="local_files_data"):
        self.directory = directory

    def create_file_datasource_if_not_exist(self):
        # Check if users.json exists, create it if not, create it
        if not os.path.isfile(self.__get_file_path()):
            with open(self.__get_file_path(), "w") as file:
                json.dump({}, file, indent=4)

    def register(self, username, password):

        self.create_file_datasource_if_not_exist()

        with open(self.__get_file_path(), "r") as file:
            users = json.load(file)

        # Check if the username already exists
        if username in users:
            return "Username is taken", False
        else:
            print("Username is available. You can add it.")

            # Add the new user
            users[username] = {"username": username, "password": password}

            # Save the updated data back to the JSON file
            with open(self.__get_file_path(), "w") as file:
                json.dump(users, file, indent=4)

        return "User registered successfully", True

    def login(self,username,password):
        try:
            self.create_file_datasource_if_not_exist()

            # Open and read the JSON file
            with open(self.__get_file_path(), 'r') as file:
                users = json.load(file)

            # Check credentials
            if username in users and users[username]["password"] == password:
                return "Login succeeded", True

            return "Invalid credentials, please try again", False

        except FileNotFoundError:
            print("File not found error.")
            return "Please register before trying to log in"

        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"

    def get_users(self):
        self.create_file_datasource_if_not_exist()

        # Open and read the JSON file
        with open(self.__get_file_path(), 'r') as file:
            users = json.load(file)

        return users

    def __get_file_path(self):
        return os.path.join(self.directory, "users.json")


