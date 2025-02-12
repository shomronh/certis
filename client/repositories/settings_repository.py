
import json
import os

from repositories.abstract_repository import AbstractRepository


class SettingsRepository(AbstractRepository):

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
        super().__init__(directory, "", "settings.json")
        self._create_folder()

    def update_scheduler_settings(self, user_id, settings):

        try:
            self._lock.acquire()

            file_path = self._get_file_path_per_user(user_id)

            if not self.is_path_exists(file_path):
                data = {}
            else:
                data = self._read_file_per_user(user_id)

            data["scheduler"] = settings

            self._write_file_per_user(user_id, data)

            return "scheduler settings updated successfully", True
        finally:
            self._lock.release()

    def get_user_settings(self, user_id):
        try:
            self._lock.acquire()

            file_path = self._get_file_path_per_user(user_id)

            if not self.is_path_exists(file_path):
                data = {}
            else:
                data = self._read_file_per_user(user_id)

            return data
        finally:
            self._lock.release()

