import logging
from demand_db import DemandDB
from datetime import datetime
import random

# Setup logging to stdout
logger = logging.getLogger(__name__)

# Open a writable database.
db = DemandDB(writable=True)



def function_handler(event, context):
    logger.info("Received message {}".format(event))
    bean = event['bean']
    quantity = event['quantity']
    timestamp = datetime.fromisoformat(event['timestamp'])
    operation = 'demand'
    db.add_delta(timestamp=timestamp, bean=bean, quantity=float(quantity), operation=operation)
