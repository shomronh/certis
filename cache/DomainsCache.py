import threading
import copy


class DomainsCache:

    _instance = None
    _lock = threading.Lock()

    __dict = {}

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def set(self, key, value):
        with self._lock:
            cloned_value = copy.deepcopy(value)
            self.__dict[key] = cloned_value

    def get(self, key):
        with self._lock:
            if key in self.__dict:
                return self.__dict[key]

            # Else
            return None