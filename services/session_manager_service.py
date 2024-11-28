
import threading

class SessionManagerService:

    # static variables
    _instance: 'SessionManagerService' = None
    _lock = threading.Lock()

    # other variables

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = cls.__new__(cls)
                cls._instance.__init()
        return cls._instance

    # to avoid creation an object usually which will then call
    # then __init__ method we can rais an RuntimeError
    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self):
        pass

    def validate_session(self, session, user_id):

        if not user_id or " " in user_id or len(user_id) == 0:
            return False

        if "username" not in session:
            return False

        username = session.get('username')
        if user_id != username:
            return False

        return True

