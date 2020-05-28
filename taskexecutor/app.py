import subprocess
import logging
import requests
import sys
import time
import redis

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
output_log = logging.StreamHandler(sys.stdout)
output_log.setLevel(logging.DEBUG)
output_log.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(output_log)

while True:
    time.sleep(1)
    try:
        queue_url = 'http://localhost:5002/todos/request'
        response = requests.get(queue_url)
        if response.status_code == 200:
            task = response.json()
            if not task:
                logger.info(f"No task fetched from queue")
                continue
            process = subprocess.run(
                task['command'], shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            logger.info(f"taskId: {task['taskId']}")
            logger.info(f"command: {task['command']}")
            logger.info(f"Output: {process.stdout}")
            if process.stderr:
                logger.error(f"Error: {str(process.stderr)}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
