import logging
import time
from dataclasses import dataclass

import requests
from jenkins import Jenkins

logger = logging.getLogger(__name__)


class JenkinsClient:
    def __init__(self, jenkins_base_url, username=None, password=None, token=None, insecure=False, build_number=None):
        self._insecure = insecure
        self._password = password
        self._token = token
        self._username = username
        self._jenkins_base_url = jenkins_base_url
        self._build_number = build_number
        self.get_server_instance()

    def get_server_instance(self):
            try:
                if (self._username and self._password):
                    return Jenkins(self._jenkins_base_url, self._username, self._password)
                elif (self._username and self._token):
                    return Jenkins(self._jenkins_base_url, self._username, self._token)
                elif (self._username and not (self._password or self._token)):
                    return Jenkins(self._jenkins_base_url, self._username)
                else:
                    return Jenkins(self._jenkins_base_url)
            except Exception as e:
                logger.info(msg='Unable to connect to Jenkins server')

    def get_job_details(self):
        server = self.get_server_instance()
        list_job = server.get_jobs()
        return list_job

    def get_build_status(self):
        try:
            response = self.server.get_build_info(self._username, self._build_number)
            return response
        except Exception as e:
            logger.info('Unable to fetch build information')
