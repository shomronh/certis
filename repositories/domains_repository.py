import json
import os
import threading

class DomainsRepository:

    def __init__(self, directory="local_files_data"):
        self.directory = directory
        self.lock = threading.Lock()

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def add_domain(self, user_id: str, domain: str):

        domains_table = self.get_domains(user_id)

        if domain in domains_table:
            return f"Domain {domain} already exists.", False

        domains_table[domain] = {"domain": domain, "status": "Pending", "last_check": "N/A", "status_error": "N/A"}

        self.__save_domains(user_id, domains_table)

        return f"Domain {domain} added successfully", True

    def get_domains(self, user_id: str):
        file_path = self.__get_file_path(user_id)

        if not os.path.exists(file_path):
            domains = {}
        with open(file_path, "r") as file:
            domains = json.load(file)

        items = []
        for key, value in domains.items():
            items.append(value)

        return items

    def __save_domains(self, user_id: str, domains_table: dict[str, any]):
        file_path = self.__get_file_path(user_id)
        with open(file_path, "w") as file:
            json.dump(domains_table, file, indent=4)

    def update_domain_status(self, user_id: str, domain_dict: dict[str, any]):

        domains_table = self.get_domains(user_id)
        domain = domain_dict["domain"]

        if domain in domains_table:
            domains_table[domain] = domain_dict
            self.__save_domains(user_id, domains_table)
        else:
            raise ValueError(f"Domain '{domain}' not found for user '{user_id}'.")

    def __get_file_path(self, user_id: str):
        return os.path.join(self.directory, f"{user_id}_domains.json")
