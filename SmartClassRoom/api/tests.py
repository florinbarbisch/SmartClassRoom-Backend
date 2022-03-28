from django.test import TestCase
from rest_framework.test import APIClient

from .models import Classroom, MeasurementStation, Measurement, ConnectionHistory
from django.contrib.auth.models import User


# No tests for Users and Groups, since we didn't create them. (django.contrib.auth.models created them)

class SmartclassroomTestCase(TestCase):
    def setUp(self):
        # create user
        User.objects.create_user(username='admin', password='admin')

        self.client = APIClient()

        response = self.client.post('/api/token/', {'username': 'admin', 'password': 'admin'})
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        Classroom.objects.create(name="Classroom 1", description="Description 1", room_number="1")
        Classroom.objects.create(name="Classroom 2", description="Description 2", room_number="2")
        Classroom.objects.create(name="Classroom 3", description="Description 3", room_number="3")

        MeasurementStation.objects.create(fk_classroom=Classroom.objects.get(name="Classroom 1"),
                                          name="Measurement Station 1", active=True)
        MeasurementStation.objects.create(fk_classroom=Classroom.objects.get(name="Classroom 1"),
                                          name="Measurement Station 2", active=True)
        MeasurementStation.objects.create(fk_classroom=Classroom.objects.get(name="Classroom 2"),
                                          name="Measurement Station 3", active=True)


class Classroom_Get(SmartclassroomTestCase):
    """
    Tests GET-Endpoint for Classrooms
    """

    def test_get_all_classrooms(self):
        response = self.client.get('/api/Classrooms/', format='json')

        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['name'], 'Classroom 3')
        self.assertEqual(response.data['results'][0]['description'], 'Description 3')
        self.assertEqual(response.data['results'][0]['room_number'], '3')

    def test_get_one_classrooms(self):
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        response = self.client.get(f'/api/Classrooms/{classroom_1.id}/', format='json')
        self.assertEqual(response.data['name'], 'Classroom 1')
        self.assertEqual(response.data['description'], 'Description 1')
        self.assertEqual(response.data['room_number'], '1')


class Classroom_Post(SmartclassroomTestCase):
    """
    Tests POST-Endpoint for Classrooms
    """

    def test_post_classroom(self):
        self.client.post('/api/Classrooms/',
                         {'name': 'Classroom 4', 'description': 'Description 4', 'room_number': '4'}, format='json')
        classroom_4 = Classroom.objects.get(name='Classroom 4')
        self.assertIsNotNone(classroom_4)
        self.assertEqual(classroom_4.name, 'Classroom 4')
        self.assertEqual(classroom_4.description, 'Description 4')
        self.assertEqual(classroom_4.room_number, '4')


class Classroom_Delete(SmartclassroomTestCase):
    """
    Tests DELETE-Endpoint for Classrooms
    """

    def test_post_classroom(self):
        classroom_3 = Classroom.objects.get(name='Classroom 3')
        self.client.delete(f'/api/Classrooms/{classroom_3.id}/', format='json')
        self.assertEqual(Classroom.objects.count(), 2)
        self.assertEqual(Classroom.objects.filter(name='Classroom 3').count(), 0)


class Classroom_Put(SmartclassroomTestCase):
    """
    Tests PUT-Endpoint for Classrooms
    """

    def test_put_classroom(self):
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        self.client.put(f'/api/Classrooms/{classroom_1.id}/',
                        {'name': 'Classroom 1a', 'description': 'Description 1a', 'room_number': '1a'}, format='json')
        classroom_1a = Classroom.objects.get(name='Classroom 1a')
        self.assertIsNotNone(classroom_1a)
        self.assertEqual(classroom_1a.name, 'Classroom 1a')
        self.assertEqual(classroom_1a.description, 'Description 1a')
        self.assertEqual(classroom_1a.room_number, '1a')


# CRUD Tests for MeasurementStation
class MeasurementStation_Get(SmartclassroomTestCase):
    """
    Tests GET-Endpoint for MeasurementStations
    """

    def test_get_measurement_station(self):
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        measurement_station_1 = MeasurementStation.objects.get(name='Measurement Station 1')
        response = self.client.get(f'/api/MeasurementStations/{measurement_station_1.id}/', format='json')
        self.assertEqual(response.data['name'], 'Measurement Station 1')
        self.assertEqual(response.data['active'], True)
        self.assertEqual(response.data['fk_classroom'], f'http://testserver/api/Classrooms/{classroom_1.id}/')


class MeasurementStation_Post(SmartclassroomTestCase):
    """
    Tests POST-Endpoint for MeasurementStations
    """

    def test_post_measurement_station(self):
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        self.client.post('/api/MeasurementStations/',
                         {'name': 'Measurement Station 4', 'active': True,
                          'fk_classroom': f'http://testserver/api/Classrooms/{classroom_1.id}/'},
                         format='json')
        measurement_station_4 = MeasurementStation.objects.get(name='Measurement Station 4')
        self.assertIsNotNone(measurement_station_4)
        self.assertEqual(measurement_station_4.name, 'Measurement Station 4')
        self.assertEqual(measurement_station_4.active, True)
        self.assertEqual(measurement_station_4.fk_classroom.id, classroom_1.id)


class MeasurementStation_Delete(SmartclassroomTestCase):
    """
    Tests DELETE-Endpoint for MeasurementStations
    """

    def test_delete_measurement_station(self):
        measurement_station_1 = MeasurementStation.objects.get(name='Measurement Station 1')
        self.client.delete(f'/api/MeasurementStations/{measurement_station_1.id}/', format='json')
        self.assertEqual(MeasurementStation.objects.count(), 2)
        self.assertEqual(MeasurementStation.objects.filter(name='Measurement Station 1').count(), 0)


class MeasurementStation_Put(SmartclassroomTestCase):
    """
    Tests PUT-Endpoint for MeasurementStations
    """

    def test_put_measurement_station(self):
        classroom_2 = Classroom.objects.get(name='Classroom 2')
        measurement_station_1 = MeasurementStation.objects.get(name='Measurement Station 1')
        self.client.put(f'/api/MeasurementStations/{measurement_station_1.id}/',
                        {'name': 'Measurement Station 1a', 'active': False,
                         'fk_classroom': f'http://testserver/api/Classrooms/{classroom_2.id}/'}, format='json')
        measurement_station_1a = MeasurementStation.objects.get(name='Measurement Station 1a')
        self.assertIsNotNone(measurement_station_1a)
        self.assertEqual(measurement_station_1a.name, 'Measurement Station 1a')
        self.assertEqual(measurement_station_1a.active, False)
        self.assertEqual(measurement_station_1a.fk_classroom.name, 'Classroom 2')
