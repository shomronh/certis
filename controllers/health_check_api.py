from http import HTTPStatus

from flask import Flask, jsonify


class HealthCheckApi:

    def initRoutes(self, app: Flask):
        @app.route('/', methods=['GET'])
        def main():
            return jsonify({"message": 'hello from certis app'}), HTTPStatus.OK

        @app.route('/healthcheck', methods=['GET'])
        def health_check():
            return jsonify({"message": 'certis healthcheck ok'}), HTTPStatus.OK