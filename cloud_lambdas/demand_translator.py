import logging
import json
import boto3
from datetime import datetime, timezone

# Setup logging to stdout
logger = logging.getLogger(__name__)
iot = boto3.client('iot-data')


blends = {
    "SageBrew": {
        'colombia': 0.7,
        'brazil': 0.3,
        'vietnam': 0
    },
    "ElasticBean": {
        'colombia': 0.4,
        'brazil': 0.6,
        'vietnam': 0
    },
    "CoffeeFormation": {
        'colombia': 0.0,
        'brazil': 0.0,
        'vietnam': 1
    }
}

size_multipliers = {
    'S': 1,
    'M': 1.2,
    'L': 1.6
}


def function_handler(event, context):
    print("Received message {}".format(event))

    amounts = {
        'colombia': 0,
        'brazil': 0,
        'vietnam': 0
    }

    for record in event['Records']:
        msg = json.loads(record['Sns']['Message'])

        for oi in msg['orderItems']:
            blend = blends[oi['coffeeName']]
            size = size_multipliers[oi['size']]
            number = oi['number']

            for bean in blend:
                amounts[bean] += number * blend[bean] * size
    print("Total bean consumption is {}".format(amounts))

    for bean in amounts:
        if amounts[bean] > 0:
            payload = {
                "bean": bean,
                "quantity": amounts[bean],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            print("Publishing {}".format(payload))
            iot.publish(topic="workzone/farm/demand", payload=json.dumps(payload))
