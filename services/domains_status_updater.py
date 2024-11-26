import requests
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import ssl
import socket

from repositories.domains_repository import DomainsRepository
from repositories.settings_repository import SettingsRepository


class DomainsStatusUpdater:
    # static variables
    _instance: 'DomainsStatusUpdater' = None

    # other variables

    # TODO: ensure the singleton is thread safe
    @staticmethod
    def get_instance():
        if not DomainsStatusUpdater._instance:
            DomainsStatusUpdater._instance = DomainsStatusUpdater()
            DomainsStatusUpdater._instance.__start()
        return DomainsStatusUpdater._instance

    def __start(self):
        self.domain_repository = DomainsRepository()
        self.settings_repository = SettingsRepository()

    def start_scaning(self):
        pass

    def scan_user_domains(self, user_id):
        try:
            domains_dict = self.domain_repository.get_domains(user_id)

            if not domains_dict:
                # return {"error": "No domains to scan for this user."}
                return

            domainsKeys = list(domains_dict.keys())

            # test one case for now
            first_domain_dict: dict[str, any] = domains_dict[domainsKeys[0]]

            if not "domain" in first_domain_dict:
                raise Exception("domain property is missing")

            self.scan_domain(first_domain_dict)
            self.get_ssl_properties(first_domain_dict)

            self.domain_repository.update_domain_status(user_id, first_domain_dict)

        except Exception as e:
            print(str(e))

    def scan_domain(self, domain_obj: dict[str, any]):
        try:
            domain = domain_obj["domain"]

            ip_address = socket.gethostbyname(domain)
            response = requests.get(f"https://{domain}", timeout=5)

            # status: Pending/Live/Down

            if response.status_code == 200:
                domain_obj["status"] = "Live"
                domain_obj["status_error"] = "N/A"
            else:
                domain_obj["status"] = "Failed"
                domain_obj["status_error"] = f"{response.status_code}"

        except requests.RequestException as e:
            domain_obj["status"] = "Down"
            domain_obj["status_error"] = str(e)

        domain_obj["last_checked"] = datetime.utcnow().isoformat()

        if domain_obj["status"] == "Live":
            return True

        return False

    def get_ssl_properties(self, domain_obj: dict[str, any]):
        try:
            domain: str = domain_obj["domain"]

            # Remove "https://", "http://", "www." from the URL if present
            hostname = domain.replace("https://", "")
            hostname = hostname.replace("http://", "")
            hostname = hostname.replace("www.", "")
            hostname = hostname.split("/")[0]

            # Establish a secure connection to fetch the SSL certificate
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()

            # Get the certificate's expiration date
            expiry_date_str = cert['notAfter']
            expiry_date = datetime.strptime(expiry_date_str, "%b %d %H:%M:%S %Y %Z")

            # Convert expiration date to a readable string format
            ssl_expiration = expiry_date.strftime("%Y-%m-%d %H:%M:%S")

            ssl_issuer = cert['issuer']

            # Check if the certificate is expired
            # if expiry_date < datetime.utcnow():
            #     return 'Expired', expiry_date_formatted
            # else:
            #     return 'Valid', expiry_date_formatted

            domain_obj["ssl_expiration"] = ssl_expiration
            domain_obj["ssl_issuer"] = ssl_issuer

            return True

        except Exception as e:
            domain_obj["ssl_expiration"] = "N/A"
            domain_obj["ssl_issuer"] = "N/A"

        return False