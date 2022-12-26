# import logging

from jenkins import Jenkins
from utils import get_json

# logger = logging.getLogger(__name__)

class JenkinsClient:
    def __init__(self, jenkins_base_url, username=None, password=None, token=None, insecure=False, build_number=None):
        self._insecure = insecure
        self._password = password
        self._token = token
        self._username = username
        self._jenkins_base_url = jenkins_base_url
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
                print(msg='Unable to connect to Jenkins server')
                raise e

    def get_jobs(self):
        jobs = self.get_server_instance().get_jobs()
        return jobs

    def get_info(self):
        info = self.get_server_instance().get_info()
        return info

    def get_nodes(self):
        list_node = self.get_server_instance().get_nodes()
        return list_node

    def list_plugin(self):
        list_plugin = self.get_server_instance().list_plugin()
        return list_plugin

    def get_views(self):
        list_view = self.get_server_instance().get_views()
        return list_view

    def is_folder(self, job_name):
        is_folder = self.get_server_instance().is_folder(job_name)
        return is_folder

    def get_all_jobs(self):
        all_job = self.get_server_instance().get_all_jobs()
        return all_job
    
    def get_list_job(self):
        all_job = self.get_server_instance().get_all_jobs()
        list_job_name = []
        for i in all_job:
            job_name = get_json('fullname', i)
            list_job_name.append(job_name)
        return list_job_name

    def build_info(self, jobname, build_number):
        build_info = self.get_server_instance().get_build_info(jobname, build_number)
        return build_info

    def get_list_build(self, jobname):
        if self.get_server_instance().is_folder(jobname):
            print(jobname+' is folder, has no build data')
        else:
            job_info = self.get_server_instance().get_job_info(jobname)
            build_object = get_json('builds', job_info)
            list_build = []
            try:
                for i in build_object:
                    build_number = get_json('number', i)
                    list_build.append(build_number)
                return list_build
            except TypeError:
                print("Job {} has no build data, {}  is not iterable".format(jobname, list_build))
    

