import os
import threading

from dotenv import load_dotenv, dotenv_values


class EnvVariablesHandler:
    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables
    __BACKEND_URL = "BACKEND_URL"
    __is_dev_mode = True

    __already_initialized = False
    __already_started = False
    __logger: "LogsService" = None

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    # to avoid creation an object usually which will then call
    # then __init__ method we can rais an RuntimeError
    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def init(self, logger: "LogsService"):
        with self._lock:
            if self.__already_initialized:
                return
            self.__already_initialized = True
            self.__logger = logger

    def start(self):

        with self._lock:
            if self.__already_started:
                return
            self.__already_started = True

            # if not found default is dev
            env = os.getenv('CERTIS_BACKEND_ENV', 'dev')

            # testing
            # env = "prod"

            if env == 'dev':
                self.__is_dev_mode = True
                load_dotenv('.env.dev')
                self.__logger.log(f".env.dev loaded")
            elif env == 'prod':
                self.__is_dev_mode = False
                project_directory = os.getcwd()
                path = os.path.join(project_directory, '.env.prod')
                load_dotenv(path)
                self.__logger.log(f"path={path} loaded, dotenv_values={dotenv_values(path)}")
            else:
                raise ValueError("Unknown environment")

            self.__logger.log(f"BACKEND_URL={os.getenv(self.__BACKEND_URL)}")

    def get_backend_url(self):
        return os.getenv(self.__BACKEND_URL)

    def is_dev_mode(self):
        return self.__is_dev_mode
