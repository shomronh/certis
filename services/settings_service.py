from jobs.domains_scanner.users_domains_scanner_job import UsersDomainsScannerJob
from repositories.settings_repository import SettingsRepository


class SettingsService:

    def __init__(self):
        self.settingsRepository = SettingsRepository()

    def update_scheduler_settings(self, user_id, settings):

        if not user_id or ' ' in user_id or len(user_id) == 0:
            return 'Empty or Invalid user_id', False

        if not settings or len(settings) == 0:
            return 'Empty or Invalid settings', False

        results = self.settingsRepository.update_scheduler_settings(user_id, settings)

        UsersDomainsScannerJob.get_instance().re_schedule_job(user_id)

        return results