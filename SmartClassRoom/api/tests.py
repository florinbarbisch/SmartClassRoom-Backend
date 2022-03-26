from msilib.schema import Class
from django.test import TestCase


from .models import Classroom, MeasurementStation, Measurement, ConnectionHistory

class Classroom_Create(TestCase):
    def setUp(self):
        Classroom.objects.create(name="Classroom 1", description="Description 1", room_number="1")
        Classroom.objects.create(name="Classroom 2", description="Description 2", room_number="2")
        Classroom.objects.create(name="Classroom 3", description="Description 3", room_number="3")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        one = Classroom.objects.get(room_number="1")
        two = Classroom.objects.get(room_number="2")
        three = Classroom.objects.get(room_number="3")
        self.assertEqual(one.name, 'Classroom 1')
        self.assertEqual(two.name, 'Classroom 2')
        self.assertEqual(three.name, 'Classroom 3')