
import threading

from flask.sessions import SessionMixin

class SessionHandler:

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
        pass
    
    def login(self, username: str, session: SessionMixin):
        session['username'] = username

    def logout(self, session: SessionMixin):
        session.clear()

    def get_username(self, session: SessionMixin):
        return session.get('username')

    def validate_session(self, session: SessionMixin, user_id: str | None = None):
        
        if "username" not in session:
            return False

        if not user_id:
            # if user_id is not passed but still we have a username 
            # from the session => just return True
            return True

        if not user_id or " " in user_id or len(user_id) == 0:
            return False

        username = session.get('username')
        if user_id != username:
            return False

        return True

