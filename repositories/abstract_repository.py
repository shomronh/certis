import threading
from abc import ABC

from utils.files_utils import FilesUtils


class AbstractRepository(ABC):

    _lock = threading.Lock()

    __directory: str
    __file_name: str
    __file_name_postfix: str

    def _init(self, directory, file_name: str, file_name_postfix: str):
        self.__directory = directory
        self.__file_name = file_name
        self.__file_name_postfix = file_name_postfix
        self._lock = threading.Lock()

        self._create_folder()

    def _create_folder(self, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            FilesUtils.create_folder(self.__directory)
        finally:
            if use_lock:
                self._lock.release()

    def _get_file_path(self):
        return FilesUtils.get_file_path(self.__directory, self.__file_name)

    def _get_file_path_per_user(self, user_id: str):
        return FilesUtils.get_file_path(self.__directory, f"{user_id}_{self.__file_name_postfix}")

    def _create_file_if_not_exist(self):
        try:
            self._lock.acquire()
            FilesUtils.create_json_file_if_not_exist(self._get_file_path())
        finally:
            self._lock.release()

    def _read_file(self, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            data = FilesUtils.read_json_file(self._get_file_path())
            return data
        finally:
            if use_lock:
                self._lock.release()

    def _write_file(self, data: any, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            FilesUtils.write_json_file(self._get_file_path(), data)
        finally:
            if use_lock:
                self._lock.release()

    def _read_file_per_user(self, user_id: str, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            data = FilesUtils.read_json_file(self._get_file_path_per_user(user_id))
            return data
        finally:
            if use_lock:
                self._lock.release()

    def _write_file_per_user(self, user_id: str, data: any, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            FilesUtils.write_json_file(self._get_file_path_per_user(user_id), data)
        finally:
            if use_lock:
                self._lock.release()

    def is_path_exists(self, path):
        return FilesUtils.is_path_exists(path)