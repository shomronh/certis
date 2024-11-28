from flask import jsonify, Request
import threading
from jobs.domains_scanner.users_domains_scanner_job import UsersDomainsScannerJob
from repositories.users_repository import UsersRepository


class RegisterService:

    # static variables
    _instance: 'RegisterService' = None
    _lock = threading.Lock()

    # other variables

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = cls.__new__(cls)
                cls._instance.__init()
        return cls._instance

    # to avoid creation an object usually which will then call
    # then __init__ method we can rais an RuntimeError
    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self):
        self.usersRepository = UsersRepository.get_instance()

    def register(self, username, password):

        # Validations
        if not username or ' ' in username or len(username) == 0 or len(username) <= 3:
            return 'Empty or Invalid username', False

        if not password or ' ' in password or len(password) == 0 or len(password) <= 3:
            return 'Empty or Invalid password', False

        message, is_ok = self.usersRepository.register(username, password)

        if is_ok:
            UsersDomainsScannerJob.get_instance().add_new_job(username)

        return message, is_ok

