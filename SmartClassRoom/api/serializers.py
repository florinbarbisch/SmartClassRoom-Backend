from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Measurement, Classroom, MeasurementStation


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
        fields = ['name', 'description', 'room_number', 'updated_on']


class MeasurementStationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MeasurementStation
        fields = ['Station_Name', 'location', 'ip_address', 'Classroom']


class MeasurementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measurement
        fields = ['Station', 'measurement_co2', 'measurement_time', 'measurement_humidity']
