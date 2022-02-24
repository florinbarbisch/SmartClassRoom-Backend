from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Metric, Classroom, MessurementStation

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
        fields = ['classroom_name', 'description', 'room_number']


class MessurementStationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MessurementStation
        fields = ['Station_Name', 'location']
        

class MessurementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metric
        fields = ['Station', 'time' , 'co2_value']