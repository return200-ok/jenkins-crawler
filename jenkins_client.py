import logging

from jenkins import Jenkins

logger = logging.getLogger(__name__)

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
                logger.info(msg='Unable to connect to Jenkins server')
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
    
    def get_list_job_name(self):
        all_job = self.get_server_instance().get_all_jobs()
        list_job_name = []
        for i in all_job:
            list_job_name.append(i['fullname'])
        return list_job_name

    def build_info(self, jobname, build_number):
        build_info = self.get_server_instance().get_build_info(jobname, build_number)
        return build_info

    def get_total_build(self, jobname):
        job_info = self.get_server_instance().get_job_info(jobname)
        list_build = job_info['builds']
        total_build_id = []
        for i in list_build:
            total_build_id.append(i['number'])
        return total_build_id
    

