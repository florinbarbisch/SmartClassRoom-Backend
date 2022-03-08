import paho.mqtt.client as mqtt
import json
from datetime import datetime

client_id = 'mqtt_django_backend'


def on_connect(client, userdata, flags, rc):
    print('Trying to connect')
    print(rc)
    if rc == 0:
        client.subscribe("fhnw/classroom/x/")
    else:
        print("Bad connection - Returned code=", rc)


def on_message(client, userdata, msg):
    payload = str(msg.payload.decode("utf-8"))
    topic = msg.topic
    qos = msg.qos
    retain = msg.retain

    print("Payload: ", payload)

    data = json.loads(payload)

    from api.models import MeasurementStation, Measurement
    s = MeasurementStation.objects.get(name='x raspberry')
    m = Measurement(fk_measurement_station=s, measurement_time=datetime.now(), time=datetime.now(), co2=data['co2'],
                    temperature=data['temperature'], humidity=data['humidity'], motion=data['motion'],
                    light=data['light'])

    m.save()


client = mqtt.Client(client_id)
client.username_pw_set('8e0v0tanDPfBzeKkuasrarRQUKwN0WQW0EiPXg2oV6NiaossmIKmXp2HYnlO9ZAZ', '')
client.on_message = on_message
client.on_connect = on_connect
client.connect("mqtt.flespi.io", 1883, 1)
