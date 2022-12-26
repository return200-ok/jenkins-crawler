#!/usr/bin/python

import logging
import os
import sys
import time
from datetime import datetime, timedelta

import rfc3339
import yaml
from dotenv import load_dotenv
from influx_client import InfluxClient
from jenkins_client import JenkinsClient
from jenkins_collector import (JenkinsCollector, Repository, collector,
                               push_data)

# '''
# Config logging handler
# '''
# def get_date_string(date_object):
#   return rfc3339.rfc3339(date_object)

# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# rootLogger = logging.getLogger()
# fileName = get_date_string(datetime.now())+'_jenkins_collecter'
# logPath = 'logs'
# fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
# fileHandler.setFormatter(logFormatter)

# '''
#     Avoid duplicated logs
# '''
# if (rootLogger.hasHandlers()):
#     rootLogger.handlers.clear()
# rootLogger.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler(sys.stdout)
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)
# logging.getLogger().setLevel(logging.DEBUG)

'''
    Load env
'''
load_dotenv()
jenkins_url = os.getenv('JENKINS_URL')
jenkins_user = os.getenv('JENKINS_USER')
jenkins_password = os.getenv('JENKINS_PASSWORD')
jenkins_insecure = os.getenv('JENKINS_INSECURE')

influx_token = os.getenv('INFLUX_TOKEN')
influx_server = os.getenv('INFLUX_DB')
org_name = os.getenv('INFLUX_ORG')
bucket_name = os.getenv('BUCKET_NAME')
logPath = os.getenv('COLLECTOR_LOG_PATH')

def main():
    jenkins_client = JenkinsClient(
        jenkins_url, jenkins_user, jenkins_password, jenkins_insecure
    )
    influx_client = InfluxClient(
        influx_server, influx_token, org_name, bucket_name
    )
    collector(jenkins_client, influx_client)

if __name__ == "__main__":
    main()
