from jobs.domains_scanner.users_domains_scanner_job import UsersDomainsScannerJob
from repositories.settings_repository import SettingsRepository
import threading


class SettingsService:

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

    # to avoid creation an object usually which will then call
    # then __init__ method we can rais an RuntimeError
    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __init(self):
        self.settingsRepository = SettingsRepository.get_instance()

    def update_scheduler_settings(self, user_id, settings):

        if not user_id or ' ' in user_id or len(user_id) == 0:
            return 'Empty or Invalid user_id', False

        if not settings or len(settings) == 0:
            return 'Empty or Invalid settings', False

        message, is_ok = self.settingsRepository.update_scheduler_settings(user_id, settings)

        if is_ok:
            UsersDomainsScannerJob.get_instance().re_schedule_job(user_id)

        return message, is_ok
