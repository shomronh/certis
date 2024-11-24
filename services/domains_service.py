import requests
import socket
import re
from datetime import datetime

from repositories.domains_repository import DomainsRepository


class DomainsService:
    def __init__(self):
        self.domain_repository = DomainsRepository()

    def add_domain(self, user_id, domain):

        # Validations
        if not user_id or ' ' in user_id or len(user_id) == 0 or len(user_id) <= 3:
            return 'Empty or Invalid username', False

        if not self.is_valid_domain(domain):
            return "Invalid domain format", False

        cleanedDomain = self.clean_domain(domain)
        result = self.domain_repository.add_domain(user_id, cleanedDomain)

        return result
    
    def get_domains(self, user_id):

        # Validations
        if not user_id or ' ' in user_id or len(user_id) == 0 or len(user_id) <= 3:
            return 'Empty or Invalid username', False

        result = self.domain_repository.get_domains(user_id)

        return result


    def is_valid_domain(self, domain):
        """Validate domain format using a regex."""

        if not domain or ' ' in domain or len(domain) == 0:
            return False

        domain = self.clean_domain(domain.lower())

        # pattern = re.compile(r'^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/[^\s]*)?$')
        pattern = re.compile(
            r"^(?:[a-zA-Z0-9]"  # Start with alphanumeric character
            r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)"  # Middle characters
            r"+[a-zA-Z]{2,}$"  # Top-level domain
        )
        match = pattern.match(domain)

        return match

    def clean_domain(self, url: str):
        # Regular expression to remove "http://" or "https://"
        return re.sub(r'^https?://', '', url)