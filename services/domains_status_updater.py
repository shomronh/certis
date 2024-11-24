import requests
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

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
        self.executor = ThreadPoolExecutor(max_workers=5)

    def scan_domains(self, user_id):
        domains = self.domain_repository.get_domains(user_id)
        if not domains:
            return {"error": "No domains to scan for this user."}

        def scan(domain):
            try:
                ip_address = socket.gethostbyname(domain)
                response = requests.get(f"http://{domain}", timeout=5)
                result = {
                    "status": "OK",
                    "ip": ip_address,
                    "http_status": response.status_code,
                    "last_checked": datetime.utcnow().isoformat()  # Current UTC timestamp
                }
            except socket.gaierror:
                result = {
                    "status": "Failed",
                    "error": "DNS resolution failed",
                    "last_checked": datetime.utcnow().isoformat()
                }
            except requests.RequestException as e:
                result = {
                    "status": "Failed",
                    "error": str(e),
                    "last_checked": datetime.utcnow().isoformat()
                }

            self.domain_repository.update_monitoring_results(user_id, domain, result)
            return result

        results = list(self.executor.map(scan, domains))
        return results