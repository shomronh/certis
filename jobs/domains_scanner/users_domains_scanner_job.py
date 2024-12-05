import os
import queue
import threading
import time

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from jobs.domains_scanner.user_domains_scanner import UserDomainsScanner
from repositories.domains_repository import DomainsRepository
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
        self.__domain_repository = DomainsRepository.get_instance()
        self.__settings_repository = SettingsRepository.get_instance()

        self.__scheduler = BackgroundScheduler()
        self.__is_started = False

        self.__users_queues_table: dict[str, queue.Queue] = {}
        self.__users = {}

        self.__delta_t_increment = 2

        # thread_pool = ThreadPoolExecutor(min(len(self.__users), 5))
        # thread_pool = ThreadPoolExecutor(max_workers=40)
        logical_cores = os.cpu_count()
        self.__thread_pool = ThreadPoolExecutor(max_workers=logical_cores)

    def start(self):

        if self.__is_started:
            return

        self.__is_started = True

        is_testing = True

        if is_testing:
            self.__users = {"test1": {}}
            thread_pool = ThreadPoolExecutor(min(len(self.__users), 1))
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
        self.__users_queues_table[user_id] = queue.Queue()

    def __start_user_domains_scanning(self, user_id: str, user_queue: queue.Queue, delta_t: int):
        self.__logger.log(f"starting user_id={user_id} job \n")

        scanner = UserDomainsScanner()
        scanner.scan_user_domains(user_id, user_queue)

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

        user_queue = self.__users_queues_table[user_id]

        delta_t = job_index * self.__delta_t_increment + seconds

        self.__scheduler.add_job(
            self.__start_user_domains_scanning,
            'interval',
            # max_instances=1,
            seconds=delta_t,
            id=f"{user_id}",
            args=[user_id, user_queue, delta_t])



    def re_schedule_job(self, user_id):
        try:
            self.__scheduler.remove_job(user_id)

            total_jobs = len(self.__scheduler.get_jobs())
            self.__add_schedular_job(user_id, total_jobs)

        except Exception as err:
            self.__logger.log(f"try to reschedule job but get error: {err}")

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
            self.__logger.log(f"try to add new job but get error: {err}")




