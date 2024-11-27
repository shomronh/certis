from flask import jsonify, Request

from jobs.domains_scanner.users_domains_scanner_job import UsersDomainsScannerJob
from repositories.users_repository import UsersRepository


class RegisterService:

    # static variables
    _instance: 'RegisterService' = None

    # other variables

    # TODO: ensure the singleton is thread safe
    @staticmethod
    def get_instance():
        if not RegisterService._instance:
            RegisterService._instance = RegisterService()
        return RegisterService._instance

    def __init__(self):
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

