from django.contrib.auth.models import User, Group
from .models import Classroom, MeasurementStation, Measurement
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer, GroupSerializer, ClassroomSerializer, MeasurementStationSerializer, MeasurementsSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassroomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class MeasurementStationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = MeasurementStation.objects.all()
    serializer_class = MeasurementStationSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeasurementsSerializer(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementsSerializer
    permission_classes = [permissions.IsAuthenticated]
