from abc import ABC

import json
import os
import threading

class AbstractRepository(ABC):

    _lock = threading.Lock()

    __directory: str
    __file_name: str
    __file_name_postfix: str

    def _init(self, directory, file_name = "", file_name_postfix = ""):
        self.__directory = directory
        self.__file_name = file_name
        self.__file_name_postfix = file_name_postfix
        self._lock = threading.Lock()

        self._create_folder()

    def _create_folder(self, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            if not os.path.exists(self.__directory):
                os.makedirs(self.__directory)
        finally:
            if use_lock:
                self._lock.release()

    def _get_file_path(self):
        return os.path.join(self.__directory, self.__file_name)

    def _get_file_path_per_user(self, user_id: str):
        return os.path.join(self.__directory, f"{user_id}_{self.__file_name_postfix}")

    def _create_file_datasource_if_not_exist(self):
        try:
            self._lock.acquire()
            if not os.path.isfile(self._get_file_path()):
                with open(self._get_file_path(), "w") as file:
                    json.dump({}, file, indent=4)
                    file.flush()
        finally:
            self._lock.release()

    def _read_file(self, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()

            with open(self._get_file_path(), 'r') as file:
                data = json.load(file)
            return data
        finally:
            if use_lock:
                self._lock.release()

    def _write_file(self, data: any, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()

            with open(self._get_file_path(), "w") as file:
                json.dump(data, file, indent=4)
                file.flush()

        finally:
            if use_lock:
                self._lock.release()

    def _read_file_per_user(self, user_id: str, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            with open(self._get_file_path_per_user(user_id), 'r') as file:
                data = json.load(file)
            return data
        finally:
            if use_lock:
                self._lock.release()

    def _write_file_per_user(self, user_id: str, data: any, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            with open(self._get_file_path_per_user(user_id), "w") as file:
                json.dump(data, file, indent=4)
                file.flush()
        finally:
            if use_lock:
                self._lock.release()

    def is_path_exists(self, path):
        return os.path.exists(path)