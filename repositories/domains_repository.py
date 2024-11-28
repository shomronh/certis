import json
import os
import threading

class DomainsRepository:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables

    @classmethod
    def get_instance(cls, directory="local_files_data"):
        with cls._lock:
            if not cls._instance:
                cls._instance = cls.__new__(cls)
                cls._instance.__init(directory)
        return cls._instance

    # to avoid creation an object usually which will then call
    # then __init__ method we can rais an RuntimeError
    def __init__(self, directory="local_files_data"):
        raise RuntimeError('Call get_instance() instead')

    def __init(self, directory):
        self.__directory = directory
        self.__lock = threading.Lock()

        if not os.path.exists(self.__directory):
            os.makedirs(self.__directory)

    def add_domain(self, user_id: str, domain: str):

        try:
            self.__lock.acquire()

            domains_table = self.get_domains(user_id, False)

            if domain in domains_table and domains_table[domain]["deleted"] == "false":
                return f"Domain {domain} already exists.", False

            domains_table[domain] = {
                "domain": domain,
                "status": "Pending",
                "last_check": "N/A",
                "status_error": "N/A",
                "deleted": "false"
            }

            self.__save_domains(user_id, domains_table)

            return f"Domain {domain} added successfully", True
        finally:
            self.__lock.release()

    def delete_domain(self, user_id: str, domain: str):

        try:
            self.__lock.acquire()

            domains_table = self.get_domains(user_id, False)

            if not domain in domains_table:
                return f"Domain {domain} doesnt exists.", False

            exiting_domain = domains_table[domain]
            exiting_domain["deleted"] = "true"

            self.__save_domains(user_id, domains_table)

            return f"Domain {domain} added successfully", True
        finally:
            self.__lock.release()

    # when called from within the class set useLock to False
    def get_domains(self, user_id: str, useLock = True):
        try:
            if useLock:
                self.__lock.acquire()

            file_path = self.__get_file_path(user_id)

            if not os.path.exists(file_path):
                domains = {}
            else:
                with open(file_path, "r") as file:
                    domains = json.load(file)

            # filter
            res = {}
            for key, value in domains.items():
                if "deleted" in value and value["deleted"] == "true":
                    continue
                res[key]=value

            return domains
        finally:
            if useLock:
                self.__lock.release()

    def get_domains_list(self, user_id: str):
        try:
            self.__lock.acquire()

            file_path = self.__get_file_path(user_id)

            if not os.path.exists(file_path):
                domains = {}
            else:
                with open(file_path, "r") as file:
                    domains = json.load(file)

            items = []
            for key, value in domains.items():
                if "deleted" in value and value["deleted"] == "true":
                    continue
                items.append(value)

            return items
        except Exception as e:
            print(e)

        finally:
            self.__lock.release()

    def __save_domains(self, user_id: str, domains_table: dict[str, any]):

        # try:
            # self.__lock.acquire()

            file_path = self.__get_file_path(user_id)

            with open(file_path, "w") as file:
                json.dump(domains_table, file, indent=4)

        # finally:
        #     self.__lock.release()

    # accessed by user_domain_scanner
    def update_domain_status(self, user_id: str, domain_dict: dict[str, any]):
        try:
            self.__lock.acquire()

            domains_table_from_db = self.get_domains(user_id, False)

            domain = domain_dict["domain"]

            if domain in domains_table_from_db:
                
                # when the user domain scanner is upading data check if domain 
                # ensure to keep the deleted property from the db before updating
                # the record into the json file
                is_deleted_from_db = domains_table_from_db[domain]["deleted"]
                domain_dict["deleted"] = is_deleted_from_db

                domains_table_from_db[domain] = domain_dict

                self.__save_domains(user_id, domains_table_from_db)
            else:
                raise ValueError(f"Domain '{domain}' not found for user '{user_id}'.")
        finally:
            self.__lock.release()

    def __get_file_path(self, user_id: str):
        return os.path.join(self.__directory, f"{user_id}_domains.json")
        
