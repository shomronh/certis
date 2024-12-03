from http import HTTPStatus

from flask import Flask, jsonify


class HealthCheckApi:

    def initRoutes(self, app: Flask):

        @app.route('/healthcheck', methods=['GET'])
        def health_check():
            return jsonify({"message": 'certis healthcheck ok'}), HTTPStatus.OK