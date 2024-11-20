import threading

from flask import Flask

from register_api import RegisterApi

class CertisApp:

    # static variables
    _instance: 'CertisApp'  = None

    # other variables

    @staticmethod
    def get_instance():
        if not CertisApp._instance:
            CertisApp._instance = CertisApp()
            CertisApp._instance.__start()
        return CertisApp._instance

    # private method
    def __start(self):
        self._app = Flask(__name__)

        # will block the access to other methods
        # self.app.run(host='0.0.0.0', port=8080)

        # solution:
        # run flask in the background
        self._thread = threading.Thread(target=self._app.run, kwargs={'host': '0.0.0.0', 'port': 8080})
        self._thread.daemon = True  # Daemon thread will exit when the main program exits
        self._thread.start()
        # thread.join()

        # yes we can create routes after running the flask app

        @self._app.route('/', methods=['GET'])
        def main():
            return 'hello1'

        # APIs creations
        RegisterApi().initRoutes(self._app)

    def get_app(self):
        return self._app

    def join(self):
        self._thread.join()


if __name__ == '__main__':
    app = CertisApp().get_instance()
    app.join()
