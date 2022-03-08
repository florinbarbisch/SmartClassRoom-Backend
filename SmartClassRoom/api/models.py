from django.db import models
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.models import TimescaleModel


# Create your models here.
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    room_number = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-name"]

        def __str__(self):
            return self.name


class MeasurementStation(models.Model):
    fk_classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()

    class Meta:
        ordering = ["-name"]

        def __str__(self):
            return self.name


class Measurement(TimescaleModel):
    fk_measurement_station = models.ForeignKey(MeasurementStation, on_delete=models.CASCADE)
    measurement_time = TimescaleDateTimeField(interval="1 millisecond")
    co2 = models.DecimalField(max_digits=19, decimal_places=10)
    temperature = models.DecimalField(max_digits=19, decimal_places=10)
    humidity = models.DecimalField(max_digits=19, decimal_places=10)
    motion = models.BooleanField(default=False)
    light = models.DecimalField(max_digits=19, decimal_places=10)

    class Meta:
        ordering = ["-measurement_time"]

        def __str__(self):
            return self.measurement_time


class EntranceEvent(TimescaleModel):
    fk_measurement_station = models.ForeignKey(MeasurementStation, on_delete=models.CASCADE)
    change = models.IntegerField()
    measurement_time = TimescaleDateTimeField(interval="1 millisecond")

    class Meta:
        ordering = ["-measurement_time"]

        def __str__(self):
            return self.measurement_time
