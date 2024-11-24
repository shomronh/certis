
import json
import os
import threading

class SettingsRepository:
    def __init__(self, directory="local_files_data"):
        self.directory = directory
        self.lock = threading.Lock()
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def update_scheduler_settings(self, user_id, settings):

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

    def __get_file_path(self, user_id):
        return os.path.join(self.directory, f"{user_id}_settings.json")

