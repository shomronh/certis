import threading
from http import HTTPStatus

from flask import Flask, request, jsonify, session

from auths.session_handler import SessionHandler
from services.domains_service import DomainsService


class DomainsApi:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables
    __sessions_handler: SessionHandler

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

        # Initialize repository and service
        service = DomainsService.get_instance()
        self.__sessions_handler = SessionHandler.get_instance()

        @app.route("/domains/add", methods=["POST"])
        def add_domain():

            try:
                data = request.get_json()

                if not data:
                    return jsonify({"message": "User ID and domain are required"}), HTTPStatus.UNAUTHORIZED

                user_id = data.get("user_id")
                domain = data.get("domain")

                if not self.__sessions_handler.validate_session(session, user_id):
                    return jsonify({"message": "user need to login first"}), HTTPStatus.UNAUTHORIZED

                message, is_ok = service.add_domain(user_id, domain)

                if is_ok:
                    return jsonify({"message": message}), HTTPStatus.OK
                else:
                    # No Content = 208 meaning everything is ok but nothing was done
                    # for example the domain already exists
                    return jsonify({"message": message}), HTTPStatus.ALREADY_REPORTED
            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

        @app.route("/domains/delete", methods=["POST"])
        def delete_domain():

            try:
                data = request.get_json()

                if not data:
                    return jsonify({"message": "User ID and domain are required"}), HTTPStatus.UNAUTHORIZED

                user_id = data.get("user_id")
                domain = data.get("domain")

                if not self.__sessions_handler.validate_session(session, user_id):
                    return jsonify({"message": "user need to login first"}), HTTPStatus.UNAUTHORIZED

                message, is_ok = service.delete_domain(user_id, domain)

                if is_ok:
                    return jsonify({"message": message}), HTTPStatus.OK
                else:
                    # No Content = 208 meaning everything is ok but nothing was done
                    # for example the domain already exists
                    return jsonify({"message": message}), HTTPStatus.ALREADY_REPORTED
            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

        @app.route("/domains/user/<id>", methods=["GET"])
        def get_domains(id):

            try:
                if not self.__sessions_handler.validate_session(session, id):
                    return jsonify({"message": "user need to login first"}), HTTPStatus.UNAUTHORIZED

                results = service.get_domains(id)

                return jsonify(results), HTTPStatus.OK

            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

        @app.route("/domains/add/file", methods=["POST"])
        def bulk_upload():

            try:
                if not request.files or not request.form:
                    return jsonify({"message": "User ID and file are required"}), HTTPStatus.UNAUTHORIZED

                user_id = request.form['user_id']
                file = request.files.get("file")

                if not self.__sessions_handler.validate_session(session, user_id):
                    return jsonify({"message": "user need to login first"}), HTTPStatus.UNAUTHORIZED

                if not allowed_file(file.filename):
                    return jsonify({"message": "invalid file format or content"}), HTTPStatus.UNAUTHORIZED

                if file:
                    # Read the content of the uploaded file directly into memory
                    lines = file.read().decode('utf-8').splitlines()

                    # Iterate through each line and eliminate empty lines
                    domains = [line for line in lines if line.strip() != '']

                    message, is_ok = service.add_domains(user_id, domains)

                    if not is_ok:
                        return jsonify({"message": message}), HTTPStatus.BAD_REQUEST

                    return jsonify({"message": message}), HTTPStatus.OK
                else:
                    jsonify({"message": "No file was uploaded"}), HTTPStatus.BAD_REQUEST

                return jsonify({"message": "Bulk Upload Successful"}), HTTPStatus.OK

            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

        def allowed_file(filename):
            """Check if the file extension is allowed."""
            return "." in filename and filename.rsplit(".", 1)[1].lower() in ["txt"]