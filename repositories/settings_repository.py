
import json
import os
import threading

class SettingsRepository:
    def __init__(self, directory="local_files_data"):
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

            return "scheduler settings updated successfully", True
        finally:
            self.__lock.release()

    def get_user_settings(self, user_id):
        file_path = self.__get_file_path(user_id)

        if not os.path.exists(file_path):
            data = {}
        else:
            with open(file_path, "r") as file:
                data = json.load(file)

        return data

    def __get_file_path(self, user_id):
        return os.path.join(self.__directory, f"{user_id}_settings.json")

