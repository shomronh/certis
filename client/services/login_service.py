import threading

from flask import session

from auths.session_handler import SessionHandler
from repositories.users_repository import UsersRepository


class LoginService:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__init()
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self):
        self.usersRepository = UsersRepository.get_instance()
        self.__session_handler = SessionHandler.get_instance()

    def login(self, username, password):

        # Validations
        if not username or ' ' in username or len(username) == 0 or len(username) <= 3:
            return 'Empty or Invalid username', False

        if not password or ' ' in password or len(password) == 0 or len(password) <= 3:
            return 'Empty or Invalid password', False

        message, is_ok = self.usersRepository.login(username, password)

        if is_ok:
            self.__session_handler.login(username, session)

        return message, is_ok
    
    def logout(self):
        self.__session_handler.logout(session)