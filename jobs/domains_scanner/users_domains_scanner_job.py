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
        self.usersRepository = UsersRepository()
        self.domain_repository = DomainsRepository()
        self.settings_repository = SettingsRepository()

        # Initialize BackgroundScheduler with the executor configuration

        self.scheduler = BackgroundScheduler()

        self.is_started = False

        self.delta_t_increment = 2

    def start(self):

        if self.is_started:
            return

        self.is_started = True

        # self.users = self.usersRepository.get_users()
        self.users = {"test1": {}}

        thread_pool = ThreadPoolExecutor(min(len(self.users), 5))
        self.scheduler.add_executor(thread_pool, alias='default')

        index = 0
        for user_id in self.users.keys():
            index += 1
            self.__add_schedular_job(user_id, index)

        self.scheduler.start()

        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

    def __start_user_domains_scanning(self, user_id, delta_t):
        print(f"starting user_id={user_id} job \n")
        scanner = UserDomainsScanner()
        scanner.scan_user_domains(user_id)

        self.re_schedule_job(user_id)

    def __add_schedular_job(self, user_id, job_index):

        # get user settings
        settings = self.settings_repository.get_user_settings(user_id)
        seconds = settings['scheduler']['seconds']

        # if len(settings.keys()) == 0:

        # create job based on these setting

        delta_t = job_index * self.delta_t_increment + seconds

        self.scheduler.add_job(
            self.__start_user_domains_scanning,
            'interval',
            max_instances=1,
            seconds=delta_t,
            id=f"{user_id}",
            args=[user_id, delta_t])


    def re_schedule_job(self, user_id):
        self.scheduler.remove_job(user_id)

        total_jobs = len(self.scheduler.get_jobs())
        self.__add_schedular_job(user_id, total_jobs)

    def add_new_job(self, user_id):
        total_jobs = len(self.scheduler.get_jobs())
        self.__add_schedular_job(user_id, total_jobs)



