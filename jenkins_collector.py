# import logging
import time
from dataclasses import dataclass
from datetime import datetime

from influx_client import InfluxPoint

# logger = logging.getLogger(__name__)


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

class BuildInfo:
    def __init__(self, jobname, url, timestamp, duration, estimatedDuration, queueId, result, displayName):
        self.jobname = jobname
        self.url = url
        self.timestamp = timestamp
        self.duration = duration
        self.estimatedDuration = estimatedDuration
        self.queueId = queueId
        self.result = result
        self.displayName = displayName

class JenkinsCollector(object):
    def __init__(self, jenkins_client, repositories):
        self._jenkins = jenkins_client
        self.repositories = repositories

def gen_build_data(build_info, job):
    data = BuildInfo(
        job,
        build_info['url'],
        round(build_info['timestamp']/1000),
        build_info['duration'],
        build_info['estimatedDuration'],
        build_info['queueId'],
        build_info['result'],
        build_info['displayName'],
    )
    return data


def gen_datapoint(data):
    measurement = 'jenkins'
    tags = {
        "jobname": data.jobname,
        "url": data.url,
        }
    timestamp = data.timestamp
    fields = {
        "duration": data.duration,
        "estimatedDuration": data.estimatedDuration,
        "result": data.result,
        }
    data_point = InfluxPoint(measurement, tags, fields, timestamp)._point
    return data_point

def push_data(data, influx_client):  
    data_point = gen_datapoint(data)
    try:
        influx_client.write_data(data_point)
        print("Wrote "+str(data_point)+" to bucket "+influx_client._bucket)
    except Exception as e:
        print("Problem inserting points for current batch")
        raise e

def collector(jenkins_client, influx_client):
    list_job = jenkins_client.get_list_job()
    for job in list_job:
        list_build = jenkins_client.get_list_build(job)
        try:
            for build in list_build:
                build_info = jenkins_client.build_info(job, build)
                data = gen_build_data(build_info, job)
                push_data(data, influx_client)
        except TypeError:
            print("Job {} has no build data, {}  is not iterable".format(job, list_build))

