import os
import threading
import time

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from jobs.domains_scanner.distributer.users_domains_distributer import UsersDomainsDistributer
from jobs.domains_scanner.scanner.domains_scanner import DomainsScanner
from repositories.settings_repository import SettingsRepository
from repositories.users_repository import UsersRepository
from services.logs_service import LogsService


class UsersDomainsScannerJob:

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
        self.__logger = LogsService.get_instance()
        self.__usersRepository = UsersRepository.get_instance()
        self.__settings_repository = SettingsRepository.get_instance()
        self.__users_domains_distributer = UsersDomainsDistributer.get_instance()

        self.__scheduler = BackgroundScheduler()
        self.__is_started = False

        # TODO: ensure dict is thread safe as well
        # self.__users_queues_table: dict[str, queue.Queue] = {}
        self.__users = {}

        self.__delta_t_increment = 2

        logical_cores = os.cpu_count()
        self.__thread_pool = ThreadPoolExecutor(max_workers=logical_cores)

    def start(self):

        if self.__is_started:
            return

        self.__is_started = True

        is_testing = False

        if is_testing:
            self.__users = self.__usersRepository.get_users()

            if len(self.__users) > 1:
                self.__users = [self.__users[0]]

            total_workers = min(len(self.__users), 1)
            if total_workers < 1:
                total_workers = 1

            self.__thread_pool = ThreadPoolExecutor(total_workers)
        else:
            self.__users = self.__usersRepository.get_users()

            if len(self.__users) == 0:
                self.__is_started = False
                return

        # populate table of users queues
        for user_id in self.__users.keys():
            self.add_queue_for_user(user_id)

        self.__scheduler.add_executor(self.__thread_pool, alias='default')

        index = 0
        for user_id in self.__users.keys():
            self.__add_schedular_job(user_id, index)

        self.__scheduler.start()

        try:
            # avoid blocking the main thread
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.__scheduler.shutdown()

    def add_queue_for_user(self, user_id: str):
        self.__users_domains_distributer.add_queue_for_user(user_id)

    def __start_domains_scanning(self, user_id: str, users_domains_distributer: UsersDomainsDistributer, delta_t: int):
        self.__logger.log(f"starting job triggered by user_id={user_id} \n")

        scanner = DomainsScanner()
        scanner.scan_user_domains(users_domains_distributer)

        # TODO: dispose scanner after completion
        # TODO: use pool of objects to avoid intensive objects creation

        self.re_schedule_job(user_id)

    def __add_schedular_job(self, user_id, job_index):

        # get user settings
        settings = self.__settings_repository.get_user_settings(user_id)

        if "scheduler" in settings and "seconds" in settings['scheduler']:
            seconds = settings['scheduler']['seconds']
        else:
            seconds = 5

        delta_t = seconds
        if delta_t < 5:
            delta_t = 5

        self.__scheduler.add_job(
            self.__start_domains_scanning,
            'interval',
            # max_instances=1,
            seconds=delta_t,
            id=f"{user_id}",
            args=[user_id, self.__users_domains_distributer, delta_t])



    def re_schedule_job(self, user_id):
        try:
            self.__scheduler.remove_job(user_id)

            total_jobs = len(self.__scheduler.get_jobs())
            self.__add_schedular_job(user_id, total_jobs)

        except Exception as err:
            self.__logger.exception(f"try to reschedule job but get error: {err}")

    def add_new_job(self, user_id):
        try:
            if not self.__is_started:
                self.start()
                self.__is_started = True

            self.__logger.log(f"add new job for {user_id}")
            total_jobs = len(self.__scheduler.get_jobs())
            self.add_queue_for_user(user_id)
            self.__add_schedular_job(user_id, total_jobs)
        except Exception as err:
            self.__logger.exception(f"try to add new job but get error: {err}")




