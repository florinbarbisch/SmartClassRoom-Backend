import paho.mqtt.client as mqtt

client_id = 'AA0aHiQwMQALKwAmNSUDDSw'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("channels/1665323/subscribe/fields/field1")
    else:
        print("Bad connection Returned code=", rc)


def on_message(client, userdata, msg):
    json = str(msg.payload.decode("utf-8"))
    topic = msg.topic
    qos = msg.qos
    retain = msg.retain
    print(json)
    from api.models import Classroom
    c = Classroom(name='sample', description='sample', room_number='sample', updated_on='sample')
    c.save()


client = mqtt.Client(client_id)
client.username_pw_set('AA0aHiQwMQALKwAmNSUDDSw', 'iSBiT09UpVgBzX0lHzp52hPH')
client.on_message = on_message
client.on_connect = on_connect
client.connect("mqtt3.thingspeak.com", 1883, 1)
