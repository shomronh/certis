import os
import json
import threading

from flask import jsonify


class UsersRepository:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables

    @classmethod
    def get_instance(cls, directory="local_files_data"):
        with cls._lock:
            if not cls._instance:
                cls._instance = cls.__new__(cls)
                cls._instance.__init(directory)
        return cls._instance

    # to avoid creation an object usually which will then call
    # then __init__ method we can rais an RuntimeError
    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self, directory):
        self.__directory = directory
        self.__lock = threading.Lock()

        if not os.path.exists(self.__directory):
            os.makedirs(self.__directory)

        self.create_file_datasource_if_not_exist()

    def register(self, username, password):

        try:
            self.__lock.acquire()

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

        finally:
            self.__lock.release()

    def login(self,username,password):
        try:
            self.__lock.acquire()

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
        finally:
            self.__lock.release()

    def get_users(self):
        try:
            self.__lock.acquire()

            # Open and read the JSON file
            with open(self.__get_file_path(), 'r') as file:
                users = json.load(file)

            return users

        finally:
            self.__lock.release()

    def __get_file_path(self):
        return os.path.join(self.__directory, "users.json")
    
    def create_file_datasource_if_not_exist(self):
        if not os.path.isfile(self.__get_file_path()):
            with open(self.__get_file_path(), "w") as file:
                json.dump({}, file, indent=4)


