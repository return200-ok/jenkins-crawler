import logging
import sys
from datetime import datetime

import rfc3339

'''
Config logging handler
'''
def get_date_string(date_object):
  return rfc3339.rfc3339(date_object)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
fileName = get_date_string(datetime.now())+'_jenkins_collecter'
logPath = 'logs'
fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
fileHandler.setFormatter(logFormatter)

'''
    Avoid duplicated logs
'''
if (rootLogger.hasHandlers()):
    rootLogger.handlers.clear()
rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
logging.getLogger().setLevel(logging.INFO)
# logger = logging.getLogger('jenkins_collector')

def get_json(element, json_data):
  try:
    if element in json_data:
      return json_data[element]
  except Exception as e:
    raise e
    
