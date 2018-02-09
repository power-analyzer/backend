from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Device(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def add_or_get_circuit_id(self, relative_id):
        circuitQuery = Circuit.objects.filter(device=self)\
            .filter(relative_id=relative_id)
        if len(circuitQuery) >= 1:
            return circuitQuery[0]
        else:
            new_circuit = Circuit()
            new_circuit.relative_id = relative_id
            new_circuit.device = self
            new_circuit.save()
            return new_circuit


class Circuit(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    relative_id = models.IntegerField()
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Circuit: " + self.name


class Measurement(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    # Note: If we choose to allow the device to set the time of measurement
    # this will have to be changed to a value that can be set.
    time = models.DateTimeField(auto_now_add=True)
    power = models.FloatField()
    voltage = models.FloatField()
    current = models.FloatField()
    phase = models.FloatField()

    def __str__(self):
        return str(self.time)
