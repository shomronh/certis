import requests
import socket
from concurrent.futures import ThreadPoolExecutor


class DomainService:
    def __init__(self, domain_repository):
        self.domain_repository = domain_repository
        self.executor = ThreadPoolExecutor(max_workers=5)

    def add_domain(self, user_id, domain):
        # Validate domain
        if not domain.startswith("http://") and not domain.startswith("https://"):
            return {"error": "Invalid domain. Must start with http:// or https://"}

        domains = self.domain_repository.get_domains(user_id)
        if domain in domains:
            return {"error": "Domain already exists."}

        self.domain_repository.save_domain(user_id, domain)
        return {"message": f"Domain {domain} added successfully."}

    def scan_domains(self, user_id):
        domains = self.domain_repository.get_domains(user_id)
        if not domains:
            return {"error": "No domains to scan for this user."}

        def scan(domain):
            try:
                ip_address = socket.gethostbyname(domain)
                response = requests.get(f"http://{domain}", timeout=5)
                return {"domain": domain, "status": "OK", "ip": ip_address, "http_status": response.status_code}
            except socket.gaierror:
                return {"domain": domain, "status": "Failed", "error": "DNS resolution failed"}
            except requests.RequestException as e:
                return {"domain": domain, "status": "Failed", "error": str(e)}

        # Use threads for parallel scanning
        results = list(self.executor.map(scan, domains))
        return results
