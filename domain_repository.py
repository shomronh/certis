import json
import os
import threading

class DomainRepository:
    def __init__(self, directory="user_data"):
        self.directory = directory
        self.lock = threading.Lock()
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def _get_file_path(self, user_id):
        return os.path.join(self.directory, f"{user_id}_domains.json")

    def _read_user_data(self, user_id):
        file_path = self._get_file_path(user_id)
        if not os.path.exists(file_path):
            return {}
        with self.lock, open(file_path, "r") as file:
            return json.load(file)

    def _write_user_data(self, user_id, data):
        file_path = self._get_file_path(user_id)
        with self.lock, open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def save_domain(self, user_id, domain, monitoring_results=None):
        """Save a domain for the user, optionally with monitoring results."""
        monitoring_results = monitoring_results or {}
        data = self._read_user_data(user_id)

        if "domains" not in data:
            data["domains"] = {}

        data["domains"][domain] = monitoring_results
        self._write_user_data(user_id, data)

    def get_domains(self, user_id):
        """Retrieve all domains for a user."""
        data = self._read_user_data(user_id)
        return data.get("domains", {})

    def update_monitoring_results(self, user_id, domain, results):
        """Update monitoring results for a specific domain."""
        data = self._read_user_data(user_id)
        if "domains" in data and domain in data["domains"]:
            data["domains"][domain] = results
            self._write_user_data(user_id, data)
        else:
            raise ValueError(f"Domain '{domain}' not found for user '{user_id}'.")
