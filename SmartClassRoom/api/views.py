from django.contrib.auth.models import User, Group
from .models import Classroom, ConnectionHistory, MeasurementStation, Measurement, EntranceEvent
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer, GroupSerializer, ClassroomSerializer, MeasurementStationSerializer, MeasurementsSerializer, ConnectionHistorySerializer, EntranceEventSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows classrooms to be viewed or edited.
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class MeasurementStationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows measurement stations to be viewed or edited.
    """
    queryset = MeasurementStation.objects.all()
    serializer_class = MeasurementStationSerializer


class MeasurementsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows measurements to be viewed or edited.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementsSerializer

    def get_queryset(self):
        queryset = Measurement.objects.all()
        fk_classroom = self.request.query_params.get('fk_classroom')
        if fk_classroom is not None:
            queryset = queryset.filter(fk_measurement_station__fk_classroom=fk_classroom)
        return queryset


class ConnectionHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows connection history to be viewed or edited.
    """
    queryset = ConnectionHistory.objects.all()
    serializer_class = ConnectionHistorySerializer
    
    def get_queryset(self):
        queryset = ConnectionHistory.objects.all()
        fk_classroom = self.request.query_params.get('fk_classroom')
        if fk_classroom is not None:
            queryset = queryset.filter(fk_measurement_station__fk_classroom=fk_classroom)
        return queryset


class EntranceEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows entrance events to be viewed or edited.
    """
    queryset = EntranceEvent.objects.all()
    serializer_class = EntranceEventSerializer

    def get_queryset(self):
        queryset = EntranceEvent.objects.all()
        fk_classroom = self.request.query_params.get('fk_classroom')
        if fk_classroom is not None:
            queryset = queryset.filter(fk_measurement_station__fk_classroom=fk_classroom)
        return queryset
