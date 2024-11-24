from flask import jsonify, Request

from repositories.users_repository import UsersRepository


class LoginService:

    def __init__(self):
        self.usersRepository = UsersRepository()

    def login(self, username, password):

        # Validations
        if not username or ' ' in username or len(username) == 0 or len(username) <= 3:
            return 'Empty or Invalid username', False

        if not password or ' ' in password or len(password) == 0 or len(password) <= 3:
            return 'Empty or Invalid password', False

        result = self.usersRepository.login(username, password)

        return result