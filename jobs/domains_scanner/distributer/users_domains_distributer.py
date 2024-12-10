
import queue
import threading

from jobs.domains_scanner.distributer.user_domains_iterator import UserDomainsIterator
from repositories.users_repository import UsersRepository

class UserDomainItem:
    user_id: str
    domain: any

class UsersDomainsDistributer:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables
    __users_queues_table: dict[str, UserDomainsIterator]
    __users_domains_collections_queue: queue.Queue[UserDomainItem]

    __users_repository: UsersRepository

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__init()
        return cls._instance
    
    def __init__(self):
        raise RuntimeError('Call get_instance() instead')
    
    def __init(self):
        self.__users_queues_table = {}
        self.__users_domains_collections_queue = queue.Queue()
        self.__users_repository = UsersRepository.get_instance()

    def add_queue_for_user(self, user_id: str):

        # if user already exists => return
        if user_id in self.__users_queues_table:
            return

        # else add it
        self.__users_queues_table[user_id] = UserDomainsIterator(user_id)

    def get_next_domain(self):
        try:
            if self.__users_domains_collections_queue.qsize() == 0:
                self.__populate_global_queue_with_users_data()

            if self.__users_domains_collections_queue.qsize() != 0:
                return self.__users_domains_collections_queue.get()

            return None
        except Exception as e:
            return None
        
    def __populate_global_queue_with_users_data(self):

        # get all users
        users = self.__users_repository.get_users()

        # for each user load its domains and insert them into its queue
        for user in users:
            self.add_queue_for_user(user)

        for user_id in self.__users_queues_table:

            next_user_domain = self.__users_queues_table[user_id].get_next_domain()

            if next_user_domain:

                item = UserDomainItem()
                item.user_id = user_id
                item.domain = next_user_domain

                self.__users_domains_collections_queue.put(item)