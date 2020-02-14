import logging
import sys
from threading import Timer


# Setup logging to stdout
logger = logging.getLogger(__name__)

def function_handler(event, context):
    logger.info("Received message {}".format(event))
