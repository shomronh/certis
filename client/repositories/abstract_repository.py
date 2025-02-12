import threading
from abc import ABC

from logger.logs_handler import LogsHandler
from files.files_corruptions_handler import FilesCorruptionsHandler
from files.files_utils import FilesUtils


class AbstractRepository(ABC):

    _lock = threading.Lock()

    _directory: str
    _file_name: str
    _file_name_postfix: str

    _logger: LogsHandler

    def __init__(self, directory, file_name: str, file_name_postfix: str):

        self._logger = LogsHandler.get_instance()

        self._directory = directory
        self._file_name = file_name
        self._file_name_postfix = file_name_postfix
        self._lock = threading.Lock()

        self._create_folder()

    def _create_folder(self, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            FilesUtils.create_folder(self._directory)
        except Exception as e:
            self._logger.exception(f"{e}")
        finally:
            if use_lock:
                self._lock.release()

    def _get_file_path(self):
        return FilesUtils.get_file_path(self._directory, self._file_name)

    def _get_file_path_per_user(self, user_id: str):
        return FilesUtils.get_file_path(self._directory, self._get_file_name_per_user(user_id))

    def _get_file_name_per_user(self, user_id: str):
        return f"{user_id}_{self._file_name_postfix}"

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
            data = FilesCorruptionsHandler.read_json_file(self._get_file_path())
            return data
        finally:
            if use_lock:
                self._lock.release()

    def _write_file(self, data: any, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            FilesCorruptionsHandler.write_json_file(
                self._directory,
                self._file_name,
                data)
        finally:
            if use_lock:
                self._lock.release()

    def _read_file_per_user(self, user_id: str, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            data = FilesCorruptionsHandler.read_json_file(self._get_file_path_per_user(user_id))
            return data
        finally:
            if use_lock:
                self._lock.release()

    def _write_file_per_user(self, user_id: str, data: any, use_lock = False):
        try:
            if use_lock:
                self._lock.acquire()
            FilesCorruptionsHandler.write_json_file(
                self._directory,
                self._get_file_name_per_user(user_id),
                data)
        finally:
            if use_lock:
                self._lock.release()

    def is_path_exists(self, path):
        return FilesUtils.is_path_exists(path)