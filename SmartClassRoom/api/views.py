from django.contrib.auth.models import User, Group
from .models import Classroom, ConnectionHistory, MeasurementStation, Measurement
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer, GroupSerializer, ClassroomSerializer, MeasurementStationSerializer, MeasurementsSerializer, ConnectionHistorySerializer


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
    API endpoint that allows classrooms to be viewed or edited.
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeasurementStationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows measurement stations to be viewed or edited.
    """
    queryset = MeasurementStation.objects.all()
    serializer_class = MeasurementStationSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeasurementsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows measurements to be viewed or edited.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementsSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConnectionHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows connection history to be viewed or edited.
    """
    queryset = ConnectionHistory.objects.all()
    serializer_class = ConnectionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
