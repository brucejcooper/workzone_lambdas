import boto3
from requests_sigv4 import Sigv4Request
import requests 
import json
from uuid import uuid4
import time




def function_handler(event, context):
    print(event)
    request = Sigv4Request(region="ap-southeast-2")

    body = {
        "orderId": str(uuid4()),
        "orderItems": [{
            "coffeeName": "SageBrew",
            "number": 1,
            "size": "L"
        }],
        "timestamp": "{}-{}-{}T{}:{}:{}Z".format(*time.gmtime()[0:6]),
        "orderPayable": 10.4
    }
    r = request.post("https://p61g8x9yl5.execute-api.ap-southeast-2.amazonaws.com/master/orders", json=body)

    if not r.ok:
        raise Exception("Error invoking: {}".format(r.content))


if __name__== "__main__":
    function_handler({}, None)