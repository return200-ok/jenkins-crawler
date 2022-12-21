import datetime
import logging
import time
from dataclasses import dataclass

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



    
