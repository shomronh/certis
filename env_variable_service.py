import os
import threading
from dotenv import load_dotenv

class EnvVariablesService:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables
    __BACKEND_URL = "BACKEND_URL"

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__init()
        return cls._instance

    # to avoid creation an object usually which will then call
    # then __init__ method we can rais an RuntimeError
    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self):

        # if not found default is dev
        env = os.getenv('CERTIS_BACKEND_ENV', 'dev')

        if env == 'dev':
            full_path = os.path.join(os.getcwd(), ".env.dev")
            load_dotenv(full_path, verbose=True)
            print(f"full_path=${full_path} loaded")
        elif env == 'prod':
            full_path = os.path.join(os.getcwd(), ".env.prod")
            load_dotenv(full_path, verbose=True)
            print(f"full_path=${full_path} loaded")
        else:
            raise ValueError("Unknown environment")

        print(f"BACKEND_URL={os.getenv(self.__BACKEND_URL)}")

    def get_backend_url(self):
        return os.getenv(self.__BACKEND_URL)