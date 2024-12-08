import socket
import ssl
import time
from datetime import datetime

import requests

from jobs.domains_scanner.distributer.users_domains_collector import UsersDomainsCollector
from repositories.domains_repository import DomainsRepository
from services.logs_service import LogsService


class DomainsScanner:

    def __init__(self):
        self.domain_repository = DomainsRepository.get_instance()   
        self.__logger = LogsService.get_instance()

    def scan_user_domains(self, users_domains_collector: UsersDomainsCollector):
        try:
            next_domain = users_domains_collector.get_next_domain()

            if not next_domain:
                self.__logger.log(f"No existing domains currently")
                return

            t0 = time.time()

            self.do_scans(next_domain.user_id, next_domain.domain)
            
            time_diff = time.time() - t0
            self.__logger.log(f"Scanning domain={next_domain.domain["domain"]} for userId={next_domain.user_id} took {time_diff} seconds")

        except Exception as e:
            self.__logger.log(str(e))

    def do_scans(self, user_id, domain_obj: dict[str, any]):

        if not "domain" in domain_obj:
            self.__logger.log("domain property is missing, skipping")
            return

        if not "deleted" in domain_obj:
            self.__logger.log("deleted property is missing, skipping")
            return

        domain = domain_obj["domain"]
        deleted = domain_obj["deleted"]

        if deleted == "true":
            self.__logger.log(f"domain={domain} considered deleted, no need to monitor")
            return

        self.__logger.debug(f"start scan user_id={user_id} domain={domain}")

        self.scan_domain(domain_obj)
        self.get_ssl_properties(domain_obj)

        self.domain_repository.update_domain_status(user_id, domain_obj)

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
