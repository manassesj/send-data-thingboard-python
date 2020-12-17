from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
import base64
import json

def hello(event, context):


    telemetry = []

    for result in event['Records']:
        base64_message = result['kinesis']['data']
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')

        message = json.loads(message)

        if message['heat_index'] != 0:
            celsius  = (message['heat_index'] - 32) / 1.8

            if celsius <= 27.0:
                message['warning'] = "Normal"
            elif celsius >= 27.0 and celsius <= 32.0:
                message['warning'] = "Caution"
            elif  celsius >= 32.1 and celsius <= 41.0:
                message['warning'] = "Extreme caution"
            elif celsius >= 41.1 and celsius <= 54.0:
                message['warning'] = "Danger"
            else:
                message['warning'] = "Extreme danger"

            message['heat_index'] = celsius


        else:
            message['warning'] = "Normal"
        telemetry.append(message)

    print(telemetry)

    try:
        #telemetry = [{"uf": "fd","index": 20.5}, {"uf": "df","index": 110.5}]
        client = TBDeviceMqttClient("demo.thingsboard.io", "ONISUjegn6ndL5GBIHNf")
        client.connect()

        for station in telemetry:
            print(station)
            result = client.send_telemetry(station)
            #print(result)
            success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
            #print(success)
        client.disconnect()



    except:
        print("Unable to send telemetry")

    # serverless invoke local --function hello