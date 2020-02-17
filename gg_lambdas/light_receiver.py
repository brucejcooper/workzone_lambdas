import logging
from demand_db import DemandDB
from datetime import datetime
import random

# Setup logging to stdout
logger = logging.getLogger(__name__)

# Open a writable database.
db = DemandDB(writable=True)


def strip_nanos(val):
    dot = val.rindex('.')
    nanos = int(val[dot+1:-1])
    micros = int(nanos / 1000)
    return "{}.{:06d}".format(val[0:dot], micros)
    

def function_handler(event, context):
    logger.info("Received message {}".format(event))

    payload = event['payload_fields']
    device = event['dev_id']
    bean = device[5:]
    tsstring = event["metadata"]["time"]
    # The timestamp provided has a timezone and nanoseconds, and a Zulu timezone on it, 
    # which Python doesn't understand.  Strip the last 4 characters off
    timestamp = datetime.fromisoformat(strip_nanos(tsstring))

    if "light" in payload:
        db.add_light_intensity_measurement(timestamp=timestamp, bean=bean, light=payload["light"])

    if "moisture" in payload:
        db.add_moisture_measurement(timestamp=timestamp, bean=bean, moisture_level=payload["moisture"])

    if "battery" in payload:
        db.record_battery_level(timestamp, device, payload["battery"])
