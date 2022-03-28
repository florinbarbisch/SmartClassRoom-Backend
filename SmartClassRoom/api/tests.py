from django.test import TestCase
from rest_framework.test import APIClient

from .models import Classroom, MeasurementStation, Measurement, ConnectionHistory

class Classroom_Create(TestCase):
    def setUp(self):
        Classroom.objects.create(name="Classroom 1", description="Description 1", room_number="1")
        Classroom.objects.create(name="Classroom 2", description="Description 2", room_number="2")
        Classroom.objects.create(name="Classroom 3", description="Description 3", room_number="3")

    def test_classrooms(self):
        client = APIClient()
        response = client.get('/api/Classrooms/', format='json')
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['name'], 'Classroom 3')
        self.assertEqual(response.data['results'][0]['description'], 'Description 3')
        self.assertEqual(response.data['results'][0]['room_number'], '3')
