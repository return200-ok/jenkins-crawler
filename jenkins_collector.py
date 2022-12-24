import datetime
import logging
import time
from dataclasses import dataclass

from influx_client import InfluxPoint
from jenkins_client import JenkinsClient

logger = logging.getLogger(__name__)

def calculate_total_duration(build_data):
    total_duration = 0
    for build in build_data:
        duration = build.get("duration")
        if duration == 0:
            duration = time.time() * 1000 - build.get("timestamp")

        total_duration += duration / 1000.0
    return total_duration


@dataclass
class Repository:
    name: str
    group: str


class JenkinsCollector(object):
    def __init__(self, jenkins_client, repositories):
        self._jenkins = jenkins_client
        self.repositories = repositories

def gen_build_data(build_info):
    data = {
        "jobname": build_info[0],
        "url": build_info['url'],
        "folder": build_info.folder,
        "key": str(build_info.folder)+"_"+str(build_info.jobname),
        "timestamp": build_info['timestamp'],
        "duration": build_info['duration'],
        "estimatedDuration": build_info['estimatedDuration'],
        "queueId": build_info['queueId'],
        "result": build_info['result'],
        "displayName": build_info['displayName'],
    }
    return data


def gen_datapoint(data):
    measurement = data.measurement
    tags = {
        "jobname": data.jobname,
        "url": data.url,
        "folder": data.folder,
        "key": data.key,
        }
    timestamp = data.timestamp
    fields = {
        "duration": data.duration,
        "estimatedDuration": data.estimatedDuration,
        "queueId": data.queueId,
        "result": data.result,
        }
    data_point = InfluxPoint(measurement, tags, fields, timestamp)._point
    return data_point

def collector():
    jenkins_base_url = 'http://192.168.3.100:8080'
    user = 'admin'
    password = 'MqU9Czz8T6MXcPR'
    insecure = False

    jenkins_client = JenkinsClient(
        jenkins_base_url, user, password, insecure
    )
    total_build_id = jenkins_client.get_total_build('Bipower-dev/bipower-team-service')
    list_job_name = jenkins_client.get_list_job_name()
    build_info = jenkins_client.build_info('Bipower-dev/bipower-team-service',56)
    print(build_info)