import requests
import socket

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime
import ssl
import socket
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from jobs.domains_scanner.user_domains_scanner import UserDomainsScanner
from repositories.domains_repository import DomainsRepository
from repositories.settings_repository import SettingsRepository
from repositories.users_repository import UsersRepository


class UsersDomainsScannerJob:

    # static variables
    _instance: 'UsersDomainsScannerJob' = None

    # other variables

    # TODO: ensure the singleton is thread safe
    @staticmethod
    def get_instance():
        if not UsersDomainsScannerJob._instance:
            UsersDomainsScannerJob._instance = UsersDomainsScannerJob()
        return UsersDomainsScannerJob._instance

    def __init__(self):
        self.__usersRepository = UsersRepository()
        self.__domain_repository = DomainsRepository()
        self.__settings_repository = SettingsRepository()

        self.__scheduler = BackgroundScheduler()
        self.__is_started = False

        self.__users = {}

        self.__delta_t_increment = 2

    def start(self):

        if self.__is_started:
            return

        self.__is_started = True

        is_testing = False

        if is_testing:
            self.__users = {"test1": {}}
            thread_pool = ThreadPoolExecutor(min(len(self.__users), 1))
        else:
            self.__users = self.__usersRepository.get_users()
            thread_pool = ThreadPoolExecutor(min(len(self.__users), 5))

        self.__scheduler.add_executor(thread_pool, alias='default')

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

    def __start_user_domains_scanning(self, user_id, delta_t):
        print(f"starting user_id={user_id} job \n")
        scanner = UserDomainsScanner()
        scanner.scan_user_domains(user_id)

        # TODO: dispose scanner after completion
        # TODO: use pool of objects to avoid intensive objects creation

        self.re_schedule_job(user_id)

    def __add_schedular_job(self, user_id, job_index):

        # get user settings
        settings = self.__settings_repository.get_user_settings(user_id)

        if "scheduler" in settings and "seconds" in settings['scheduler']:
            seconds = settings['scheduler']['seconds']
        else:
            seconds = 10

        delta_t = job_index * self.__delta_t_increment + seconds

        self.__scheduler.add_job(
            self.__start_user_domains_scanning,
            'interval',
            # max_instances=1,
            seconds=delta_t,
            id=f"{user_id}",
            args=[user_id, delta_t])


    def re_schedule_job(self, user_id):
        try:
            self.__scheduler.remove_job(user_id)

            total_jobs = len(self.__scheduler.get_jobs())
            self.__add_schedular_job(user_id, total_jobs)

        except Exception as err:
            print(f"try to reschedule job but get error: {err}")

    def add_new_job(self, user_id):
        try:
            total_jobs = len(self.__scheduler.get_jobs())
            self.__add_schedular_job(user_id, total_jobs)
        except Exception as err:
            print(f"try to add new job but get error: {err}")




