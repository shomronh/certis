import requests
import socket

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime
import ssl
import socket
import time

from apscheduler.schedulers.background import BackgroundScheduler

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

        self.users = self.usersRepository.get_users()

        threadPool = ThreadPoolExecutor(min(len(self.users), 5))
        self.scheduler.add_executor(threadPool, alias='default')


        delta_t = self.delta_t_increment

        for user_id in self.users.keys():
            delta_t += self.delta_t_increment
            self.add_schedular_job(user_id, delta_t)

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

        # after completion remove the job
        self.scheduler.remove_job(f"{user_id}")

        # then re-add a job
        self.add_schedular_job(user_id, delta_t)

    def __add_schedular_job(self, user_id, delta_t):

        # get user settings

        # create job based on these setting

        self.scheduler.add_job(
            self.__start_user_domains_scanning,
            'interval',
            # max_instances=1
            seconds=delta_t,
            id=f"{user_id}",
            args=[user_id, delta_t])

        pass

    def re_schedule_job(self, user_id):

        self.scheduler.pause_job(user_id)

        # get user settings

        # re schedule the job
        self.scheduler.reschedule_job(f"{user_id}")

        # then resume it
        self.scheduler.resume_job(user_id)

    def add_new_job(self, user_id):
        total_jobs = len(self.scheduler.get_jobs())
        delta_t = self.delta_t_increment * total_jobs
        self.__add_schedular_job(user_id, delta_t)



