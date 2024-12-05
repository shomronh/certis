import importlib
import logging
import threading
import coloredlogs  # Use coloredlogs instead of colorlog

from env_variable_service import EnvVariablesService


class LogsService:
    # Static variables
    _instance = None
    _lock = threading.Lock()

    __already_initialized = False
    __already_started = False

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')  # Ensure singleton pattern

    def init(self, envVariablesService: 'EnvVariablesService', name="certis_logger"):
        with self._lock:
            if self.__already_initialized:
                return
            self.__already_initialized = True

            self.__env_variables_service = envVariablesService
            self.__logger = logging.getLogger(name)

    def start(self):

        with self._lock:
            if self.__already_started:
                return
            self.__already_started = True

            # Use coloredlogs to handle the console output
            coloredlogs.install(level='DEBUG', logger=self.__logger)

            # Create file handler for logging to file
            file_handler = logging.FileHandler('logfile.log')
            file_handler.setLevel(logging.DEBUG)

            # Set up a simple formatter for file output (no color)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d',
                datefmt="%Y-%m-%d %H:%M:%S"  # Optional custom date format
            )
            file_handler.setFormatter(file_formatter)

            # Add file handler to the logger
            self.__logger.addHandler(file_handler)

            is_dev_mode = self.__env_variables_service.get_instance().is_dev_mode()

            if is_dev_mode:
                # Capture DEBUG logs in development
                self.__logger.setLevel(logging.DEBUG)
            else:
                # Capture INFO and above in production
                self.__logger.setLevel(logging.INFO)

    def log(self, msg, *args, level = logging.DEBUG, **kwargs):
        self.__logger.log(level, msg, *args, **kwargs, stacklevel=2)

    def debug(self, msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs, stacklevel=2)
    
    def info(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs, stacklevel=2)

    def warn(self, msg, *args, **kwargs):
        self.__logger.warning(msg, *args, **kwargs, stacklevel=2)

    def error(self, msg, *args, **kwargs):
        self.__logger.error(msg, *args, **kwargs, stacklevel=2)

    def critical(self, msg, *args, exc_info=True, **kwargs):
        self.__logger.critical(msg, *args, exc_info=exc_info, **kwargs, stacklevel=2)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.__logger.exception(msg, *args, exc_info=exc_info, **kwargs, stacklevel=2)


