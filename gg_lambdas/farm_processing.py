import logging
import time

import greengrasssdk
from demand_db import DemandDB
from constants import bean_names
from datetime import datetime, timezone
from threading import Thread

logger = logging.getLogger(__name__)



def bean_processing_time(bean_name):
    return 1

def run_farm(bean_name):
    ''' Runs a farm for a given bean type, producing a result every few seconds when there is demand'''
    db = DemandDB(writable=True)

    while True:
        try:
            demand = 0
            demand = db.get_current_level(bean_name)
            logger.info("Demand is %d for %s", demand, bean_name)
            if demand >= 0.001:  # Allow for epsilon
                time.sleep(bean_processing_time(bean_name))
                logger.info("Adding production for %s", bean_name)
                db.add_delta(timestamp=datetime.now(timezone.utc), bean=bean_name, quantity=-min(0.1, demand), operation='production')
            else:
                time.sleep(1)
        except Exception:
            logger.exception("Fatal error in main loop")

threads = [Thread(target=run_farm, args=(bean, )) for bean in bean_names]

for thread in threads:
    thread.start()


logger.info("Waiting for processing threads to finish (which they never should)")
for thread in threads:
    thread.join()

logger.warn("Shoulnd't get to here...")

def function_handler(event, context):
    ''' Dummy handler for long running lambda'''
    pass
