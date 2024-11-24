import os
from http import HTTPStatus

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import re
from werkzeug.utils import secure_filename
from services.domains_service import DomainsService


class DomainsApi:

    def initRoutes(self, app: Flask):

        # Initialize repository and service
        service = DomainsService()

        @app.route("/domains/add", methods=["POST"])
        def add_domain():

            try:

                # TODO: ensure that username from the session is the same as the user_id, otherwise return HTTPStatus.UNAUTHORIZED

                if "username" not in session:
                    return jsonify({"message": "user need to login first"}), HTTPStatus.UNAUTHORIZED

                data = request.get_json()

                if not data:
                    return jsonify({"message": "User ID and domain are required"}), HTTPStatus.UNAUTHORIZED

                user_id = data.get("user_id")
                domain = data.get("domain")

                message, is_ok = service.add_domain(user_id, domain)

                if is_ok:
                    return jsonify({"message": message}), HTTPStatus.OK
                else:
                    # No Content = 208 meaning everything is ok but nothing was done
                    # for example the domain already exists
                    return jsonify({"message": message}), HTTPStatus.ALREADY_REPORTED
            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR


        @app.route("/domains/bulk", methods=["POST"])
        def bulk_upload():

            try:
                if "username" not in session:
                    return jsonify({"message": "user need to login first"}), HTTPStatus.UNAUTHORIZED

                data = request.get_json()

                if not data:
                    return jsonify({"message": "User ID and file are required"}), HTTPStatus.UNAUTHORIZED

                user_id = data.get("user_id")
                file = request.files.get("file")

                if not user_id or not file:
                    return jsonify({"message": "User id and file are required"}), HTTPStatus.BAD_REQUEST

                if not allowed_file(file.filename):
                    return jsonify({"message": "invalid file format or content"}), HTTPStatus.BAD_REQUEST

                if file:
                    # Read the content of the uploaded file directly into memory
                    lines = file.read().decode('utf-8').splitlines()

                    # Iterate through each line and eliminate empty lines
                    domains = [line for line in lines if line.strip() != '']

                    for domain in domains:
                        service.add_domain(user_id, domain)
                else:
                    jsonify({"message": "No file was uploaded"}), HTTPStatus.BAD_REQUEST

                return jsonify({"message": "Bulk Upload Successful"}), HTTPStatus.OK

            except Exception as e:
                return jsonify({"message": f"Something wrong happend: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

        def allowed_file(filename):
            """Check if the file extension is allowed."""
            return "." in filename and filename.rsplit(".", 1)[1].lower() in ["txt"]