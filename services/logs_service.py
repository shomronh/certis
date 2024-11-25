import logging
from logging.handlers import RotatingFileHandler
import os 
import json
from datetime import datetime

class loggingservice:
    def __init__(self, log_dir='logs'):
          # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure logging
        self.logger = logging.getLogger('AppLogger')
        self.logger.setLevel(logging.DEBUG)
        
         # Rotating file handler
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'application.log'), 
            maxBytes=1024 * 1024 * 5,  # 5 MB
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
        # console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console_handler)

def log_event(self, user_id, event_type, details=None):
        """
        Log an event with standardized format
        
        Args:
            user_id (str): User identifier
            event_type (str): Type of event (login, register, domain_add, etc.)
            details (dict, optional): Additional event details
        """
        if not user_id or ' ' in user_id or len(user_id) <= 3:
            self.logger.error(f"Invalid user_id for logging: {user_id}")
            return False

                    
        # Prepare log entry
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'event_type': event_type,
            'details': details or {}
        }
   
         # Log the event
        self.logger.info(json.dumps(log_entry))
        return True
