import json
import os
import threading

from repositories.abstract_repository import AbstractRepository
from services.logs_service import LogsService


class UsersRepository(AbstractRepository):

    # static variables
    _instance = None

    # other variables

    @classmethod
    def get_instance(cls, directory="local_files_data"):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__init(directory)
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self, directory):
        super()._init(directory, "users.json", "")
        self.__logger = LogsService.get_instance()
        self._create_file_datasource_if_not_exist()

    def register(self, username, password):

        try:
            self._lock.acquire()

            users = self._read_file()

            # Check if the username already exists
            if username in users:
                return "Username is taken", False
            else:
                self.__logger.log("Username is available. You can add it.")

                # Add the new user
                users[username] = {"username": username, "password": password}

                self._write_file(users)

            return "User registered successfully", True

        finally:
            self._lock.release()

    def login(self,username,password):
        try:
            self._lock.acquire()

            # Open and read the JSON file
            users = self._read_file()

            # Check credentials
            if username in users and users[username]["password"] == password:
                return "Login succeeded", True

            return "Invalid credentials, please try again", False

        except FileNotFoundError:
            self.__logger.log("File not found error.")
            return "Please register before trying to log in"

        except Exception as e:
            self.__logger.log(f"An error occurred: {e}")
            return f"An error occurred: {e}"
        finally:
            self._lock.release()

    def get_users(self):
        try:
            self._lock.acquire()

            users = self._read_file()

            return users

        finally:
            self._lock.release()



