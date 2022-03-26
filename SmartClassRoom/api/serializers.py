from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Measurement, Classroom, MeasurementStation, ConnectionHistory


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Classroom
        fields = ['url', 'name', 'description', 'room_number', 'updated_on']


class MeasurementStationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MeasurementStation
        fields = ['url', 'fk_classroom', 'name', 'active', 'ip_address']


class MeasurementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measurement
        fields = ['url', 'fk_measurement_station', 'time', 'measurement_time', 'co2', 'temperature', 'humidity', 'motion', 'light']


class ConnectionHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConnectionHistory
        fields = ['url', 'fk_measurement_station', 'time', 'insert_time', 'ip_address', 'bluetooth_connected', 'wlan_signal_strength', 'ping_backend', 'ping_broker', 'ping_grafana']
