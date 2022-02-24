from django.db import models
from timescale.db.models.fields import TimescaleDateTimeField
# Create your models here.
from timescale.db.models.models import TimescaleModel


class Classroom(models.Model):
  classroom_name = models.CharField(max_length=100)
  description = models.CharField(max_length=200)
  room_number = models.CharField(max_length=100)
  
class MessurementStation(models.Model):
  Station_Name = models.CharField(max_length=50)
  Locaton = models.ForeignKey(Classroom, on_delete=models.CASCADE)
  


class Metric(TimescaleModel):
  Station = models.ForeignKey(MessurementStation, on_delete=models.CASCADE)
  co2_value = models.FloatField()
  time = TimescaleDateTimeField(interval="1 sec")