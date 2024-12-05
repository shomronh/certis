import logging
import threading
import coloredlogs  # Use coloredlogs instead of colorlog

from abstract_atom import factory_get_env_variable_service


class LogsService:
    # Static variables
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__init_logger()  # Initialize the logger only once
        return cls._instance

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')  # Ensure singleton pattern

    def __init_logger(self, name="certis_logger"):
        # Create logger instance
        self.logger = logging.getLogger(name)

        # Use coloredlogs to handle the console output
        coloredlogs.install(level='DEBUG', logger=self.logger)

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
        self.logger.addHandler(file_handler)

        is_dev_mode =

        if is_dev_mode:
            # Capture DEBUG logs in development
            self.logger.setLevel(logging.DEBUG)
        else:
            # Capture INFO and above in production
            self.logger.setLevel(logging.INFO)

    def log(self, msg, *args, **kwargs):
        self.logger.log(logging.DEBUG, msg, *args, **kwargs, stacklevel=2)

    # Logging methods for different log levels
    def debug(self, msg, *args, **kwargs):
        """Log debug messages with stacklevel=2."""
        self.logger.debug(msg, *args, **kwargs, stacklevel=2)

    def info(self, msg, *args, **kwargs):
        """Log info messages with stacklevel=2."""
        self.logger.info(msg, *args, **kwargs, stacklevel=2)

    def warn(self, msg, *args, **kwargs):
        """Log warning messages with stacklevel=2."""
        self.logger.warning(msg, *args, **kwargs, stacklevel=2)

    def error(self, msg, *args, **kwargs):
        """Log error messages with stacklevel=2."""
        self.logger.error(msg, *args, **kwargs, stacklevel=2)

    def critical(self, msg, *args, exc_info=True, **kwargs):
        """Log exception messages with stacklevel=2."""
        self.logger.critical(msg, *args, exc_info=exc_info, **kwargs, stacklevel=2)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """Log exception messages with stacklevel=2."""
        self.logger.exception(msg, *args, exc_info=exc_info, **kwargs, stacklevel=2)


