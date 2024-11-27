import os
import threading
from datetime import timedelta

from flask import Flask

from controllers.domains_api import DomainsApi
from controllers.health_check_api import HealthCheckApi
from controllers.login_api import LoginApi
from controllers.register_api import RegisterApi
from controllers.settings_api import SettingsApi
from jobs.domains_scanner.users_domains_scanner_job import UsersDomainsScannerJob


class CertisApp:

    # static variables
    _instance: 'CertisApp'  = None

    # other variables

    # TODO: ensure the singleton is thread safe
    @staticmethod
    def get_instance():
        if not CertisApp._instance:
            CertisApp._instance = CertisApp()
            CertisApp._instance.__start()
        return CertisApp._instance

    # private method
    def __start(self):
        self._app = Flask(__name__)
        self._app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

        self._app.secret_key = os.urandom(24)  # secured random key

        self.__setup_session()

        # Services bootstrap
        UsersDomainsScannerJob.get_instance()

        # APIs creations
        @self._app.route('/<filename>')
        def file(filename):
            return self._app.send_static_file(filename)

        HealthCheckApi().initRoutes(self._app)
        SettingsApi().initRoutes(self._app)
        RegisterApi().initRoutes(self._app)
        LoginApi().initRoutes(self._app)
        DomainsApi().initRoutes(self._app)

        # by default Flask enables multithreading by default

        # after calling the run() method, this will block the access
        # to other methods (ex: running testing after the run() call)
        # self._app.run(host='0.0.0.0', port=8080)

        # solution:
        # run flask in another thread

        # 'debug': True requires to run flask on main thread
        # flask_config = {'host': '0.0.0.0', 'port': 8080, 'debug': True}
        flask_config = {'host': '0.0.0.0', 'port': 8080, 'debug': False}

        # TODO: if in production mode use instead:
        # flask_config = {'host': '0.0.0.0', 'port': 8080, 'debug': False}

        self._thread = threading.Thread(target=self._app.run, kwargs=flask_config)
        self._thread.daemon = True  # Daemon thread will exit when the main program exits
        self._thread.start()

        #
        # UsersDomainsScannerJob.get_instance().start()

    def __setup_session(self):
        is_prod = False

        if is_prod:

            # Session Settings for Production:
            self._app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript from accessing cookies.
            self._app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS in production.
            self._app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Strong CSRF protection: Cookies are only sent in first-party requests.

            self._app.config['SESSION_PERMANENT'] = True  # Set sessions as permanent in production.
            self._app.permanent_session_lifetime = timedelta(minutes=30)

            self._app.config['SESSION_TYPE'] = 'redis'  # Store session data in Redis (ideal for production).
            # self._app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379)  # Connect to Redis server for session storage.

            self._app.config['SESSION_COOKIE_PATH'] = '/'  # Session cookies will be sent for all paths in the domain.

        else:
            self._app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript from accessing cookies (basic protection).
            self._app.config['SESSION_COOKIE_SECURE'] = False  # Do not enforce HTTPS in development (HTTPS may not be set up in local dev).
            self._app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevent cookies from being sent in cross-site requests (basic CSRF protection).
            self._app.config['SESSION_PERMANENT'] = False  # Sessions are not permanent by default in development.
            self._app.config['SESSION_TYPE'] = 'filesystem'  # Store session data in the file system for easy debugging.

        # to persist user data across browser sessions
        # session.permanent = True

    def get_app(self):
        return self._app

    def join(self):
        self._thread.join()



if __name__ == '__main__':
    app = CertisApp().get_instance()
    app.join()
