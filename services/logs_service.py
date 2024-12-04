
import logging
import threading


class LogsService:

    # static variables
    _instance = None
    _lock = threading.Lock()

    # other variables

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
        
        logging.basicConfig(
            level=logging.DEBUG,  
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler() # Logs to console
            ])

    def log(level, msg, *args, **kwargs):
        logging.log(msg, args, kwargs)

    def exception(msg, *args, exc_info=True, **kwargs):
        logging.exception(msg, args, exc_info, kwargs)

    def error(msg, *args, **kwargs):
        logging.error(msg, args, kwargs)
