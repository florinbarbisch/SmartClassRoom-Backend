from msilib.schema import Class
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from .models import Classroom, MeasurementStation, Measurement, ConnectionHistory

class Selinum_Test_Cases(TestCase):
    #Well i hate python for Web Testing :) Cypress is the best
    def setUp(self):
        try:
            self.driver = webdriver.Chrome('C:\\tools\selenium\chromedriver.exe')
        except:
            print("Error: Chrome driver not found")
        
        try:
            self.driver = webdriver.Firefox()
        except:
            print("Error: Chrome driver not found")
        
        try:
            self.driver = webdriver.Safari()
        except:
            print("Error: Safari driver not found")
        
        if self.driver is None:
            raise Exception("Error: No driver found")

    def test_selenium(self):
        self.driver.get("https://www.python.org")
        print(self.driver.title)
        search_bar = self.driver.find_element_by_name("q")
        search_bar.clear()
        search_bar.send_keys("getting started with python")
        search_bar.send_keys(Keys.RETURN)
        print(self.driver.current_url)
        self.assertEqual(self.driver.current_url, "https://www.python.org/search/?q=getting+started+with+python&submit=")
        self.driver.close()



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