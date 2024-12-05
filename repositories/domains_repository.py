import json
import os

from repositories.abstract_repository import AbstractRepository
from services.logs_service import LogsService


# TODO:
#  when stopping the app while we are writing the JSON file
#  it can end with wrong json we need a way to handle to use case

class DomainsRepository(AbstractRepository):

    # static variables
    _instance = None

    # other variables

    @classmethod
    def get_instance(cls, directory="local_files_data"):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__init(directory)
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self, directory):
        super()._init(directory, "", "domains.json")
        self.__logger = LogsService.get_instance()
        self._create_folder()

    # if domain exists in domains file AND deleted == "false" => return already exists
    # if domain [exists and deleted is "true"] or not => 
    def add_domain(self, user_id: str, domain: str):

        try:
            self._lock.acquire()

            domains_table = self.get_domains(user_id, False)

            if domain in domains_table and domains_table[domain]["deleted"] == "false":
                return f"Domain {domain} already exists.", False

            # exists AND deleted == "true" OR not exists
        
            domains_table[domain] = {
                "domain": domain,
                "status": "Pending",
                "last_check": "N/A",
                "status_error": "N/A",
                "deleted": "false"
            }

            self._write_file_per_user(user_id, domains_table)

            return f"Domain {domain} added successfully", True
        finally:
            self._lock.release()

    def delete_domain(self, user_id: str, domain: str):

        try:
            self._lock.acquire()

            domains_table = self.get_domains(user_id, False)

            if not domain in domains_table:
                return f"Domain {domain} doesnt exists.", False

            exiting_domain = domains_table[domain]
            exiting_domain["deleted"] = "true"

            self._write_file_per_user(user_id, domains_table)

            return f"Domain {domain} added successfully", True
        finally:
            self._lock.release()

    # when called from within the class set useLock to False
    def get_domains(self, user_id: str, useLock = True):
        try:
            if useLock:
                self._lock.acquire()

            file_path = self._get_file_path_per_user(user_id)

            if not self.is_path_exists(file_path):
                domains = {}
            else:
                domains = self._read_file_per_user(user_id)

            # filter
            res = {}
            for key, value in domains.items():
                if "deleted" in value and value["deleted"] == "true":
                    continue
                res[key]=value

            return domains
        finally:
            if useLock:
                self._lock.release()

    def get_domains_list(self, user_id: str):
        try:
            self._lock.acquire()

            file_path = self._get_file_path_per_user(user_id)

            if not self.is_path_exists(file_path):
                domains = {}
            else:
                domains = self._read_file_per_user(user_id)

            items = []
            for key, value in domains.items():
                if "deleted" in value and value["deleted"] == "true":
                    continue
                items.append(value)

            return items
        except Exception as e:
            self.__logger.log(e)

        finally:
            self._lock.release()

    # accessed by user_domain_scanner
    def update_domain_status(self, user_id: str, domain_dict: dict[str, any]):
        try:
            self._lock.acquire()

            domains_table_from_db = self.get_domains(user_id, False)

            domain = domain_dict["domain"]

            if domain in domains_table_from_db:
                
                # when the user domain scanner is upading data check if domain 
                # ensure to keep the deleted property from the db before updating
                # the record into the json file
                is_deleted_from_db = domains_table_from_db[domain]["deleted"]
                domain_dict["deleted"] = is_deleted_from_db

                domains_table_from_db[domain] = domain_dict

                self._write_file_per_user(user_id, domains_table_from_db)
            else:
                raise ValueError(f"Domain '{domain}' not found for user '{user_id}'.")
        finally:
            self._lock.release()

        
