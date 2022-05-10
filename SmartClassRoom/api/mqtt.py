import paho.mqtt.client as mqtt
import json
import random
import string
import logging
from django.utils import timezone, dateparse

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG,
                    handlers=[
                        logging.FileHandler("mqtt.log", mode="a"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)


def random_string(length):  # define the function and pass the length as argument
    return ''.join(
        (random.choice(string.ascii_lowercase) for x in range(length)))  # run loop until the define length


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))

    topics = ["fhnw/+/+/measurement",
              "fhnw/+/+/entranceevent", "fhnw/+/+/connectionhistory"]

    if rc == 0:
        for topic in topics:
            client.subscribe(topic)
            logger.info("Subscribed to topic: " + topic)
    else:
        logger.error("Bad connection - Returned code=" + str(rc))


def on_connect_fail(client, userdata, rc):
    logger.error("Connect failed with result code " + str(rc))


def on_disconnect(client, userdata, rc):
    logger.warning("On disconnect called with result code " + str(rc))

    logger.info("Calling connect again...")
    client.connect("mqtt.flespi.io", 1883, 1)


def on_reconnect(client, userdata, rc):
    logger.info("On reconnect called with result code " + str(rc))


def on_message(client, userdata, msg):
    payload = str(msg.payload.decode("utf-8"))
    topic = msg.topic
    qos = msg.qos
    retain = msg.retain
    print("Topic: ", topic, "/ ", "Payload: ", payload.strip())

    data = json.loads(payload)

    location, room_name, measurement_station_id, measurement_type = topic.split(
        '/')

    # handle different topics and classrooms
    try:
        if measurement_type == 'measurement':
            handle_measurement(data, room_name, measurement_station_id)
        elif measurement_type == 'entranceevent':
            handle_entrance_event(data, room_name, measurement_station_id)
        elif measurement_type == 'connectionhistory':
            handle_connection_history(data, room_name, measurement_station_id)
    except Exception as e:
        logger.exception(e)


def handle_entrance_event(data, room_name, measurement_station_id):
    from api.models import Classroom, MeasurementStation, EntranceEvent
    c = Classroom.objects.get(name=room_name)
    s = MeasurementStation.objects.get(
        id=measurement_station_id, fk_classroom=c.id)
    m = EntranceEvent(fk_measurement_station=s, insert_time=timezone.now(),
                      time=dateparse.parse_datetime(data['time']), change=data['change'])

    m.save()


def handle_measurement(data, room_name, measurement_station_id):
    from api.models import Classroom, MeasurementStation, Measurement
    c = Classroom.objects.get(name=room_name)
    s = MeasurementStation.objects.get(
        id=measurement_station_id, fk_classroom=c.id)
    m = Measurement(fk_measurement_station=s, insert_time=timezone.now(),
                    time=dateparse.parse_datetime(data['time']), co2=data['co2'],
                    temperature=data['temperature'], humidity=data['humidity'], motion=data['motion'],
                    light=data['light'])

    m.save()


def handle_connection_history(data, room_name, measurement_station_id):
    from api.models import Classroom, MeasurementStation, ConnectionHistory
    c = Classroom.objects.get(name=room_name)
    s = MeasurementStation.objects.get(
        id=measurement_station_id, fk_classroom=c.id)

    m = ConnectionHistory(fk_measurement_station=s, insert_time=timezone.now(),
                          time=dateparse.parse_datetime(data['time']), ip_address=data['local-ip'],
                          bluetooth_connected=data['feather-connected'],
                          wlan_signal_strength=int(
                              float(data['wlan-strength'])),
                          ping_backend=int(float(data['ping-django'])), ping_broker=int(float(data['ping-flespi'])),
                          ping_grafana=int(float(data['ping-grafana'])))

    m.save()


client_id = f'mqtt_django_backend_{random_string(5)}'
logger.info('Generated client_id: ' + client_id)

client = mqtt.Client(client_id)
client.username_pw_set(
    '8e0v0tanDPfBzeKkuasrarRQUKwN0WQW0EiPXg2oV6NiaossmIKmXp2HYnlO9ZAZ', '')
client.on_message = on_message
client.on_connect = on_connect
client.on_reconnect = on_reconnect
client.on_connect_fail = on_connect_fail
client.on_disconnect = on_disconnect
client.connect("mqtt.flespi.io", 1883, 1)
