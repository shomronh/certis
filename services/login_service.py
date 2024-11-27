from flask import jsonify, Request

from repositories.users_repository import UsersRepository


class LoginService:

    # static variables
    _instance: 'LoginService' = None

    # other variables

    # TODO: ensure the singleton is thread safe
    @staticmethod
    def get_instance():
        if not LoginService._instance:
            LoginService._instance = LoginService()
        return LoginService._instance

    def __init__(self):
        self.usersRepository = UsersRepository.get_instance()

    def login(self, username, password):

        # Validations
        if not username or ' ' in username or len(username) == 0 or len(username) <= 3:
            return 'Empty or Invalid username', False

        if not password or ' ' in password or len(password) == 0 or len(password) <= 3:
            return 'Empty or Invalid password', False

        result = self.usersRepository.login(username, password)

        return result