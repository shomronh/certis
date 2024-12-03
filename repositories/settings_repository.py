
import json
import os
import threading

class SettingsRepository:

    # static variables
    _instance = None
    _lock = threading.Lock()

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
        self.__directory = directory
        self.__lock = threading.Lock()

        if not os.path.exists(self.__directory):
            os.makedirs(self.__directory)

    def update_scheduler_settings(self, user_id, settings):

        try:
            self.__lock.acquire()

            file_path = self.__get_file_path(user_id)

            if not os.path.exists(file_path):
                data = {}
            else:
                with open(file_path, "r") as file:
                    data = json.load(file)

            data["scheduler"] = settings

            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
                file.flush()

            return "scheduler settings updated successfully", True
        finally:
            self.__lock.release()

    def get_user_settings(self, user_id):
        try:
            self.__lock.acquire()

            file_path = self.__get_file_path(user_id)

            if not os.path.exists(file_path):
                data = {}
            else:
                with open(file_path, "r") as file:
                    data = json.load(file)

            return data
        finally:
            self.__lock.release()


    def __get_file_path(self, user_id):
        return os.path.join(self.__directory, f"{user_id}_settings.json")

