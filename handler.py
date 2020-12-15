import paho.mqtt.client as paho  # mqtt library
import json

def hello(event, context):

    ACCESS_TOKEN = 'ERdDIEYFsMjunS8YSxe3'  # Token of your device
    broker = "demo.thingsboard.io"  # host name
    port = 1883  # data listening port

    def on_publish(client, userdata, result):  # create function for
        print("data published to thingsboard \n")
        pass

    client1 = paho.Client("control1")  # create client object
    client1.on_publish = on_publish  # assign function to
    client1.username_pw_set(ACCESS_TOKEN)  # access token from
    client1.connect(broker, port, keepalive=60)  # establish connection

    payload = json.dumps({
        "name": "PYTHON3",
        "index": 0
    })

    ret = client1.publish("v1/devices/me/telemetry", payload)
    print("Please check LATEST TELEMETRY field of your device")
    print(payload);
