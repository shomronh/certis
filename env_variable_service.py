import os
import threading

from dotenv import load_dotenv, find_dotenv, dotenv_values

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
        project_directory = os.getenv('CERTIS_PROJECT_DIRECTORY', '')

        print(f"env=${env} project_directory={project_directory}")

        if env == 'dev':
            path =  os.path.join(project_directory, '.env.dev')
            load_dotenv(path)
            print(f"path={path} loaded, dotenv_values={dotenv_values(path)}")
        elif env == 'prod':
            path = os.path.join(project_directory, '.env.prod')
            load_dotenv(path)
            print(f"path={path} loaded, dotenv_values={dotenv_values(path)}")
        else:
            raise ValueError("Unknown environment")
        


        print(f"BACKEND_URL={os.getenv(self.__BACKEND_URL)}")

    def get_backend_url(self):
        return os.getenv(self.__BACKEND_URL)