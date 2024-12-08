
import queue
import threading

from jobs.domains_scanner.user_domains_iterator import UserDomainsIterator
from repositories.domains_repository import DomainsRepository
from repositories.users_repository import UsersRepository

class GlobalDomainsQueueItem:
    user_id: str
    domain: any

class GlobalDomainsQueueDistributer:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables
    __users_queues_table: dict[str, UserDomainsIterator]
    __global_domains_queue: queue.Queue[GlobalDomainsQueueItem]

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
        self.__global_domains_queue = queue.Queue()
        self.__users_repository = UsersRepository.get_instance()

    def add_queue_for_user(self, user_id: str):

        # if user already exists => return
        if user_id in self.__users_queues_table:
            return

        # else add it
        self.__users_queues_table[user_id] = UserDomainsIterator(user_id)

    def get_next_domain(self):
        try:
            if self.__global_domains_queue.qsize() == 0:
                self.__populate_global_queue_with_users_data()

            return self.__global_domains_queue.get()
        except Exception as e:
            return None
        
    def __populate_global_queue_with_users_data(self):

        # get all users
        users = self.__users_repository.get_users()

        # for each user load its domains and insert them into its queue
        for user in users:
            self.add_queue_for_user(user)  
            self.__users_queues_table[user].load_domains()

        while True:

            if not self.has_more_domains_to_add():
                break

            for user_id in self.__users_queues_table:

                next_user_domain = self.__users_queues_table[user_id].get_next_domain()

                if next_user_domain:
                    item = GlobalDomainsQueueItem()
                    item.user_id = user_id
                    item.domain = next_user_domain
                    self.__global_domains_queue.put(item)

    def has_more_domains_to_add(self):
        count = 0
        for user_id in self.__users_queues_table:
            user_domains_iterator = self.__users_queues_table[user_id]
            size = user_domains_iterator.get_queue_size()
            count += size
        return count != 0