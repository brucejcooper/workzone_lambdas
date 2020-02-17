import logging
import sys
import time
from datetime import datetime, timedelta, timezone
from influxdb import InfluxDBClient
import constants 

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)




class DemandDB:
    def __init__(self, writable=False):
        self.writable = writable
        self.influx = InfluxDBClient(host='localhost', port=8086)
        self.influx.switch_database('farm')


    def get_all_current_levels(self):
        res = self.influx.query('select sum(order_qty) from demand group by bean')
        bean_names = [x[1]['bean'] for x in res.keys()]

        try:
            return { bean: next(res.get_points(tags={"bean": bean}))['sum'] for bean in bean_names}
        except StopIteration:
            return 0

    def get_current_level(self, bean):
        res = self.influx.query('select sum(order_qty) from demand where bean = $bean', bind_params={'bean': bean})
        try:
            return next(res.get_points())['sum']
        except StopIteration:
            return 0


    def add_delta(self, timestamp, bean, quantity, operation='demand'):
        self.influx.write_points([
            {
                "measurement": "demand",
                "tags": {
                    "bean": bean,
                    "operation": operation
                },
                "time": timestamp.isoformat(),
                "fields": {
                    "order_qty": quantity
                }
            }
        ])

    def add_light_intensity_measurement(self, timestamp, bean, light):
        json_body = [
            {
                "measurement": "light",
                "tags": {
                    "bean": bean,
                },
                "time": timestamp.isoformat(),
                "fields": {
                    "light": light
                }
            }
        ]
        self.influx.write_points(json_body)

    def record_battery_level(self, timestamp, device_id, battery_level):
        json_body = [
            {
                "measurement": "battery",
                "tags": {
                    "device_id": device_id
                },
                "time": timestamp.isoformat(),
                "fields": {
                    "battery_level": battery_level
                }
            }
        ]
        self.influx.write_points(json_body)

    def add_moisture_measurement(self, timestamp, bean, moisture_level):
        json_body = [
            {
                "measurement": "moisture",
                "tags": {
                    "bean": bean
                },
                "time": timestamp.isoformat(),
                "fields": {
                    "moisture_level": moisture_level
                }
            }
        ]
        self.influx.write_points(json_body)
