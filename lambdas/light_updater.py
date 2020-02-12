import logging
import time
from phue import Bridge

import greengrasssdk
from demand_db import DemandDB
from constants import bean_names

logger = logging.getLogger(__name__)


db = DemandDB(writable=False)

b = Bridge('192.168.1.131', username='YpW3N7bi7go2ARq6JKOw2LV0hUxEfO-ic4KbdQgY')
b.connect()

lights = b.get_light_objects('name')

def setup_light(light):
    light.on = True
    light.brightness = 128
    light.transitiontime = 2  # in increments of 0.1s

for light in bean_names:
    setup_light(lights[light])

def demand_to_brightness(demand):
    ''' Works out what brightness to set the light to, based upon the demand parameter'''
    return int(max(0, min(demand*17, 254)))

def update_lights():
    ''' Updates the brightness of the lights to be representative of the demand, as stored in the SQLITE database'''
    while True:
        demand = db.get_all_current_levels()
        print("Demand is {}".format(demand))
        brightness = {bean: demand_to_brightness(current_demand) for bean,current_demand in demand.items()}

        # Give it defaults if there are no rows in the result_set
        for light in bean_names:
            if light not in brightness:
                brightness[light] = demand_to_brightness(0)

        # Debug.
        logger.info(brightness)

        # Send the brightness to the individual lamps
        for bean, light_bright in brightness.items():
            light = lights[bean]
            light.brightness = light_bright
        time.sleep(0.5)

logger.info("running task")
update_lights()

logger.warn("Shoulnd't get to here...")

def function_handler(event, context):
    ''' Dummy handler for long running lambda'''
    pass
