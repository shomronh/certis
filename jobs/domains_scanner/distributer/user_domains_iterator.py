

import queue

from repositories.domains_repository import DomainsRepository


class UserDomainsIterator:

    __user_id: str
    __domains_repository: DomainsRepository
    __queue: queue.Queue

    def __init__(self, user_id):
        self.__user_id = user_id
        self.__queue = queue.Queue()
        self.__domains_repository = DomainsRepository.get_instance()

    def put(self, domain):
        self.__queue.put(domain)

    # TODO: use in memory cache to avoid inserting all domains again
    def __load_domains(self):
        domains = self.__domains_repository.get_domains(self.__user_id)
        
        for domainKey in domains:
            domainObj = domains[domainKey]
            self.__queue.put(domainObj)

    def get_next_domain(self): 

        if self.get_queue_size() == 0:
            self.__load_domains()

        if self.get_queue_size() != 0:
            return self.__queue.get()

        return None

    def get_queue_size(self):
        return self.__queue.qsize()