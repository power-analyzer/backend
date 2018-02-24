from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from datapoints.models import Device, UnarchivedMeasurement, Measurement


def get_or_add_device(mac):
    try:
        device = Device.objects.get(mac=mac)
        return device
    except ObjectDoesNotExist:
        new_device = Device()
        new_device.mac = mac
        new_device.save()
        new_device.name = "New Device " + str(new_device.id)
        new_device.save()
        return new_device

def archive_or_add_measurement(measurement):
    circuit = measurement.circuit
    unarchived_measurements = UnarchivedMeasurement.objects.filter(circuit=circuit).order_by('time')
    if len(unarchived_measurements) > 0 and \
measurement.time > unarchived_measurements.last().time + timezone.timedelta(minutes = 30):
        archive_measurements(circuit)
    measurement.save()


def archive_measurements(circuit):
    measurement = Measurement()
    measurement.circuit = circuit
    unarchived_measurements = UnarchivedMeasurement.objects.filter(circuit=circuit).order_by('time')
    # Calculate new measurement time.
    last = unarchived_measurements.last().time
    first = unarchived_measurements.first().time
    measurement.time = (last - first) / 2 + first

    #Calculate new power, voltage, and current
    dT = (last - first) / len(unarchived_measurements)
    dT = dT.total_seconds()
    for key in ["power", "voltage", "current"]:
        power = 0.0
        for umeasurement in unarchived_measurements:
            power += getattr(umeasurement, key, 0) * dT

        try:
            setattr(measurement, key, power)
        except KeyError:
            pass

    # Phase????
    # TODO: Figure this out.
    measurement.phase = unarchived_measurements.first().phase

    measurement.save()
    unarchived_measurements.delete()
