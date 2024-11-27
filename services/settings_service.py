from jobs.domains_scanner.users_domains_scanner_job import UsersDomainsScannerJob
from repositories.settings_repository import SettingsRepository
import threading


class SettingsService:

    # static variables
    _instance: 'SettingsService' = None
    _lock = threading.Lock()

    # other variables

    # TODO: ensure the singleton is thread safe
    @staticmethod
    def get_instance():
        with SettingsService._lock:
            if not SettingsService._instance:
                SettingsService._instance = SettingsService()
            return SettingsService._instance

    def __init__(self):
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
