from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Device(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Circuit(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    Circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    # Note: If we choose to allow the device to set the time of measurement
    # this will have to be changed to a value that can be set.
    time = models.DateTimeField(auto_now_add=True)
    power = models.FloatField()

    def __str__(self):
        return str(self.time)
