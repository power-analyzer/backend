from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Device(models.Model):
    mac = models.CharField(max_length=50, unique=True, null=False)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    phase_offset = models.CharField(
        max_length=30,
        choices=(("left", "Left +90"), ("right", "Right -90")),
        default="right"
    )

    def __str__(self):
        return "Device: " + self.name

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

    CT_TEN = '10A'
    CT_LIST = [
        (CT_TEN, '10 Amp Current Transformer')
    ]

    circuit_transformer_type = models.CharField(
        max_length=200,
        choices=CT_LIST,
        default=CT_TEN
    )

    pannel_side = models.CharField(
        max_length=200,
        choices=(("left", "Left Side"), ("right", "Right Side")),
        default="right"
    )

    def __str__(self):
        return "Circuit: " + self.name

class UnarchivedMeasurement(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    time = models.DateTimeField()

    # TODO: Remove `null=True` when we figure out exaclty what data will
    # be measured.
    power = models.FloatField(null=True)
    voltage = models.FloatField(null=True)
    current = models.FloatField(null=True)
    phase = models.FloatField(null=True)

    def __str__(self):
        return str(self.time)


class Measurement(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    time = models.DateTimeField()

    # TODO: Remove `null=True` when we figure out exaclty what data will
    # be measured.
    power = models.FloatField(null=True)
    voltage = models.FloatField(null=True)
    current = models.FloatField(null=True)
    phase = models.FloatField(null=True)

    def __str__(self):
        return str(self.time)
