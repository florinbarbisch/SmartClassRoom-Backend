import paho.mqtt.client as mqtt
import json
from django.utils import timezone, dateparse

client_id = 'mqtt_django_backend'


def generate_topics():
    from api.models import Classroom, MeasurementStation

    topics_to_subscribe = []
    classrooms = Classroom.objects.all()
    for classroom in classrooms:
        measurement_stations = MeasurementStation.objects.filter(fk_classroom=classroom.id)
        for measurement_station in measurement_stations:
            topics_to_subscribe.append(f"fhnw/{classroom.name}/{measurement_station.id}/measurement")
            topics_to_subscribe.append(f"fhnw/{classroom.name}/{measurement_station.id}/entrance_event")

    print('Topics List generated:', topics_to_subscribe)
    return topics_to_subscribe


def on_connect(client, userdata, flags, rc):
    topics = generate_topics()

    if rc == 0:
        for topic in topics:
            client.subscribe(topic)
            print("Subscribed to topic: ", topic)
    else:
        print("Bad connection - Returned code=", rc)


def on_message(client, userdata, msg):
    payload = str(msg.payload.decode("utf-8"))
    topic = msg.topic
    qos = msg.qos
    retain = msg.retain
    print("Topic: ", topic)
    print("Payload: ", payload)

    data = json.loads(payload)

    location, room_name, measurement_station_id, measurement_type = topic.split('/')

    # handle different topics and classrooms
    try:
        if measurement_type == 'measurement':
            handle_measurement(data, room_name, measurement_station_id)
        elif measurement_type == 'entrance_event':
            handle_entrance_event(data, room_name, measurement_station_id)
    except Exception as e:
        print(e)


def handle_entrance_event(data, room_name, measurement_station_id):
    from api.models import Classroom, MeasurementStation, EntranceEvent
    c = Classroom.objects.get(name=room_name)
    s = MeasurementStation.objects.get(id=measurement_station_id, fk_classroom=c.id)
    m = EntranceEvent(fk_measurement_station=s, measurement_time=dateparse.parse_datetime(data['time']),
                      time=timezone.now(), change=data['change'])

    m.save()


def handle_measurement(data, room_name, measurement_station_id):
    from api.models import Classroom, MeasurementStation, Measurement
    c = Classroom.objects.get(name=room_name)
    s = MeasurementStation.objects.get(id=measurement_station_id, fk_classroom=c.id)
    m = Measurement(fk_measurement_station=s, measurement_time=dateparse.parse_datetime(data['time']),
                    time=timezone.now(), co2=data['co2'],
                    temperature=data['temperature'], humidity=data['humidity'], motion=data['motion'],
                    light=data['light'])

    m.save()


client = mqtt.Client(client_id)
client.username_pw_set('8e0v0tanDPfBzeKkuasrarRQUKwN0WQW0EiPXg2oV6NiaossmIKmXp2HYnlO9ZAZ', '')
client.on_message = on_message
client.on_connect = on_connect
client.connect("mqtt.flespi.io", 1883, 1)
