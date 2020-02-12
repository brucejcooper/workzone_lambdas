#!/usr/bin/env python3

# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import random
from datetime import datetime, timezone
import time
import math





bean_names = ['colombia', 'yemen', 'vietnam']


# For certificate based connection
mqtt = AWSIoTMQTTClient("Faker")
# For Websocket connection
# mqtt = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
mqtt.configureEndpoint("atv4nltpnep7d-ats.iot.ap-southeast-2.amazonaws.com", 8883)
# For Websocket
# mqtt.configureEndpoint("YOUR.ENDPOINT", 443)
# For TLS mutual authentication with TLS ALPN extension
# mqtt.configureEndpoint("YOUR.ENDPOINT", 443)
mqtt.configureCredentials("AmazonRootCA1.pem", "0cb587de94-private.pem.key", "0cb587de94-certificate.pem.crt")
# For Websocket, we only need to configure the root CA
# mqtt.configureCredentials("YOUR/ROOT/CA/PATH")
mqtt.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
mqtt.configureDrainingFrequency(2)  # Draining: 2 Hz
mqtt.configureConnectDisconnectTimeout(10)  # 10 sec
mqtt.configureMQTTOperationTimeout(5)  # 5 sec


mqtt.connect()


while True:
    payload = {
        "bean": bean_names[math.floor(random.random()*3)],
        "quantity": 1,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    print("Publishing {}".format(payload))
    mqtt.publish("workzone/farm/demand", json.dumps(payload), 0)
    time.sleep(1.8)



