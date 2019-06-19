import logging
import datetime

# create logger with 'spam_application'
logger = logging.getLogger('peekaboologger')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('/home/pi/timelapse/peekaboologger.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def log(timeCaptured):
    logger.info(timeCaptured)   
