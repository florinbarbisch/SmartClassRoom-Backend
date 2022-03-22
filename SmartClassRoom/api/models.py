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

    class Meta:
        ordering = ["-name"]

        def __str__(self):
            return self.name


class Measurement(TimescaleModel):
    fk_measurement_station = models.ForeignKey(MeasurementStation, on_delete=models.CASCADE)
    insert_time = TimescaleDateTimeField(interval="7 days")
    co2 = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    temperature = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    humidity = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    motion = models.BooleanField(default=False, null=True)
    light = models.DecimalField(max_digits=19, decimal_places=10, null=True)

    class Meta:
        ordering = ["-insert_time"]

        def __str__(self):
            return self.insert_time


class EntranceEvent(TimescaleModel):
    fk_measurement_station = models.ForeignKey(MeasurementStation, on_delete=models.CASCADE)
    change = models.IntegerField()
    insert_time = TimescaleDateTimeField(interval="7 days")

    class Meta:
        ordering = ["-insert_time"]

        def __str__(self):
            return self.insert_time


class ConnectionHistory(TimescaleModel):
    fk_measurement_station = models.ForeignKey(MeasurementStation, on_delete=models.CASCADE)
    insert_time = TimescaleDateTimeField(interval="7 days")
    ip_address = models.GenericIPAddressField()
    bluetooth_connected = models.BooleanField(default=False, null=True)
    wlan_signal_strength = models.IntegerField()
    ping_backend = models.IntegerField()
    ping_broker = models.IntegerField()
    ping_grafana = models.IntegerField()

    class Meta:
        ordering = ["-insert_time"]

        def __str__(self):
            return self.insert_time
