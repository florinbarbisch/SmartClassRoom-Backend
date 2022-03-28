from django.test import TestCase
from rest_framework.test import APIClient

from .models import Classroom, MeasurementStation, Measurement, ConnectionHistory

class Classroom_Get(TestCase):
    """
    Tests GET-Endpoint for Classrooms
    """
    def setUp(self):
        self.client = APIClient()
        Classroom.objects.create(id=1, name="Classroom 1", description="Description 1", room_number="1")
        Classroom.objects.create(id=2, name="Classroom 2", description="Description 2", room_number="2")
        Classroom.objects.create(id=3, name="Classroom 3", description="Description 3", room_number="3")


    def test_get_all_classrooms(self):
        response = self.client.get('/api/Classrooms/', format='json')

        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['name'], 'Classroom 3')
        self.assertEqual(response.data['results'][0]['description'], 'Description 3')
        self.assertEqual(response.data['results'][0]['room_number'], '3')


    def test_get_one_classrooms(self):
        response = self.client.get('/api/Classrooms/1/', format='json')

        self.assertEqual(response.data['name'], 'Classroom 1')
        self.assertEqual(response.data['description'], 'Description 1')
        self.assertEqual(response.data['room_number'], '1')
