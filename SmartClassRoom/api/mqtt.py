import paho.mqtt.client as mqtt
#from api.models import Classroom


def on_connect(client, userdata, flags, rc):
    client.subscribe("home/mytopic")

def on_message(client, userdata, msg):
    json = str(msg.payload.decode("utf-8"))
    topic=msg.topic
    qos=msg.qos
    retain=msg.retain
    from api.models import Classroom
    c = Classroom(name='sample', description='sample', room_number='sample', updated_on='sample')
    c.save()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("public.mqtthq.com", 1883, 60)