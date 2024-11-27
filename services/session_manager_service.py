


class SessionManagerService:

    # static variables
    _instance: 'SessionManagerService' = None

    # other variables

    # TODO: ensure the singleton is thread safe
    @staticmethod
    def get_instance():
        if not SessionManagerService._instance:
            SessionManagerService._instance = SessionManagerService()
        return SessionManagerService._instance

    def __init__(self):
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

