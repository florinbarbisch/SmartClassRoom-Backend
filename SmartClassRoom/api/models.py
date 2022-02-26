from django.db import models
from timescale.db.models.fields import TimescaleDateTimeField
# Create your models here.
from timescale.db.models.models import TimescaleModel


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    roomnumber = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-name"]

        def __str__(self):
            return self.classroom_name


class MeasurementStation(models.Model):
    active = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()
    station_name = models.CharField(max_length=50)
    Classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    class Meta:
        ordering = ["-station_name"]

        def __str__(self):
            return self.station_name


class measurement(TimescaleModel):
    Station = models.ForeignKey(MeasurementStation, on_delete=models.CASCADE)
    measurement_co2 = models.DecimalField(max_digits=19, decimal_places=10)
    measurement_temperature = models.DecimalField(
        max_digits=19, decimal_places=10)
    measurement_humidity = models.DecimalField(
        max_digits=19, decimal_places=10)
    measurement_time = TimescaleDateTimeField(interval="1 sec")
    class Meta:
        ordering = ["-measurement_time"]

        def __str__(self):
            return self.classroom_name
