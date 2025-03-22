import logging
import os
from datetime import datetime

LOGS_DIR = "logs"
#create the fodler if doesn't exist and leave if folder exist
os.makedirs(LOGS_DIR, exist_ok = True)

LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y%m%d')}")

logging.basicConfig(

    filename=LOG_FILE,
    format= '%(asctime)s  - %(levelname)s - %(message)s', # format of message that shows in log file
    level=logging.INFO # there are lots of level and shows message in log file based on level defined and upper level message 
)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
