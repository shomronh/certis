import threading
from http import HTTPStatus

from flask import Flask, jsonify


class HealthCheckApi:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables

    @classmethod
    def get_instance(cls, app: Flask):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__init(app)
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self, app: Flask):
        @app.route('/healthcheck', methods=['GET'])
        def health_check():
            return jsonify({"message": 'certis healthcheck ok'}), HTTPStatus.OK