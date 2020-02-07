import logging
import sys
from threading import Timer

import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def function_handler(event, context):
    logger.info("Received message {}".format(event))
