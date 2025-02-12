import threading
from datetime import timedelta

from flask import Flask
from flask_cors import CORS

from controllers.domains_api import DomainsApi
from controllers.google_login_api import GoogleLoginApi
from controllers.health_check_api import HealthCheckApi
from controllers.login_api import LoginApi
from controllers.register_api import RegisterApi
from controllers.settings_api import SettingsApi
from globals.env_variables_handler import EnvVariablesHandler
from jobs.users_domains_scanner_job import UsersDomainsScannerJob
from logger.logs_handler import LogsHandler


class CertisApp:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables
    __app: Flask

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__start()
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    # private method
    def __start(self):

        self.create_dependencies_injections()

        self.__app = Flask(__name__)
        self.__app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB
        
        # after restart all users will be logged out
        # self.__app.secret_key = os.urandom(24)  # secured random key

        # TODO: use secret key more securely 
        # users will be kept loggedin after a restart
        self.__app.secret_key = '123456789012345678901234'


        # Enable CORS for all routes and all origins
        CORS(self.__app, 
            # supports_credentials=True,
            methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'],
             origins=['http://127.0.0.1:8080'])

        self.__setup_session()

        # self.__app.config.update(
        #     SESSION_COOKIE_SAMESITE='None',  # Allow cross-domain cookies
        #     SESSION_COOKIE_SECURE=False,     # Disable Secure flag (since you're not using HTTPS)
        #     SESSION_COOKIE_HTTPONLY=True     # Ensure the cookie is only accessible via HTTP(S), not JavaScript
        # )

        # @self.__app.after_request
        # def add_cors_headers(response):
        #     response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
        #     response.headers['Access-Control-Allow-Credentials'] = 'true'
        #     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        #     response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        #     return response

        # Services bootstrap
        # UsersDomainsScannerJob.get_instance().start()
        
        HealthCheckApi.get_instance(self.__app)
        GoogleLoginApi.get_instance(self.__app)
        SettingsApi.get_instance(self.__app)
        RegisterApi.get_instance(self.__app)
        LoginApi.get_instance(self.__app)
        DomainsApi.get_instance(self.__app)

        # by default Flask enables multithreading by default

        # after calling the run() method, this will block the access
        # to other methods (ex: running testing after the run() call)
        # self.__app.run(host='0.0.0.0', port=8080)

        # solution:
        # run flask in another thread

        # 'debug': True requires to run flask on main thread
        # flask_config = {'host': '0.0.0.0', 'port': 8080, 'debug': True}
        flask_config = {'host': '0.0.0.0', 'port': 3000, 'debug': False}

        # TODO: if in production mode use instead:
        # flask_config = {'host': '0.0.0.0', 'port': 8080, 'debug': False}

        self.__thread = threading.Thread(target=self.__app.run, kwargs=flask_config)
        self.__thread.daemon = True  # Daemon thread will exit when the main program exits
        self.__thread.start()

        UsersDomainsScannerJob.get_instance().start()

    # https://blog.miguelgrinberg.com/post/cookie-security-for-flask-applications
    def __setup_session(self):
        is_prod = False

        if is_prod:

            # Session Settings for Production:
            self.__app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript from accessing cookies.
            self.__app.config['REMEMBER_COOKIE_HTTPONLY'] = True
            self.__app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS in production.
            self.__app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Strong CSRF protection: Cookies are only sent in first-party requests.

            self.__app.config['SESSION_PERMANENT'] = True  # Set sessions as permanent in production.
            self.__app.permanent_session_lifetime = timedelta(minutes=30)

            # self.__app.config['SESSION_TYPE'] = 'redis'  # Store session data in Redis (ideal for production).
            # self.__app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379)  # Connect to Redis server for session storage.

            self.__app.config['SESSION_COOKIE_PATH'] = '/'  # Session cookies will be sent for all paths in the domain.

        else:
            self.__app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript from accessing cookies (basic protection).
            self.__app.config['REMEMBER_COOKIE_HTTPONLY'] = True
            self.__app.config['SESSION_COOKIE_SECURE'] = False  # Do not enforce HTTPS in development (HTTPS may not be set up in local dev).
            self.__app.config['SESSION_COOKIE_SAMESITE'] = 'None'  
            self.__app.config['SESSION_PERMANENT'] = True  # Sessions are not permanent by default in development.
            self.__app.config['SESSION_TYPE'] = 'filesystem'  # Store session data in the file system for easy debugging.

            self.__app.config['SESSION_COOKIE_PATH'] = '/'


    def create_dependencies_injections(self):

        # manual injections

        envVariablesHandler = EnvVariablesHandler.get_instance()
        logsService = LogsHandler.get_instance()

        envVariablesHandler.init(logsService)
        logsService.init(envVariablesHandler)

        envVariablesHandler.start()
        logsService.start()

    def join(self):
        self.__thread.join()

if __name__ == '__main__':
    app = CertisApp.get_instance()
    app.join()
