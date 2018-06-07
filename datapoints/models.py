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
        choices=(("left", "Left 0 degrees"), ("right", "Right +180 degrees")),
        default="right"
    )

    def __str__(self):
        return "Device " + str(self.id) + ": " + self.name

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
        return "Circuit " + str(self.id) + ": " + self.name

class UnarchivedMeasurement(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    time = models.DateTimeField()

    magnitude = models.FloatField()
    phase = models.FloatField()

    v_magnitude = models.FloatField()
    v_phase = models.FloatField()

    i_magnitude = models.FloatField()
    i_phase = models.FloatField()


    def __str__(self):
        return str(self.time)


class Measurement(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    time = models.DateTimeField()

    magnitude = models.FloatField()
    phase = models.FloatField()

    max_p_phase = models.FloatField(null=True)
    max_i = models.FloatField(null=True)

    v_magnitude = models.FloatField()
    v_phase = models.FloatField()

    i_magnitude = models.FloatField()
    i_phase = models.FloatField()


    def __str__(self):
        return str(self.time)


class Alert(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    last_used = models.DateTimeField()
    frequency_limit = models.IntegerField()
    max_val = models.FloatField(null=True)
    min_val = models.FloatField(null=True)
    email = models.CharField(max_length=200)
    attribute = models.CharField(
        max_length=200,
        default="magnitude",
    )
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        name = self.name if self.name else ""
        return "Alert " + str(self.id) + ": " + name
