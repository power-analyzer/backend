from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings

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
    unarchived_measurements = UnarchivedMeasurement.objects.filter(circuit=circuit).order_by('-time')
    if len(unarchived_measurements) > 0 and \
measurement.time > unarchived_measurements.last().time + timezone.timedelta(minutes = settings.ARCHIVE_TIME):
        archive_measurements(circuit)
    measurement.save()


def archive_measurements(circuit):
    measurement = Measurement()
    measurement.circuit = circuit
    unarchived_measurements = UnarchivedMeasurement.objects.filter(circuit=circuit).order_by('-time')
    # Calculate new measurement time.
    newest = unarchived_measurements.first().time
    oldest = unarchived_measurements.last().time
    measurement.time = (newest - oldest) / 2 + oldest

    #Calculate new power, voltage, and current
    dT = (newest - oldest) / len(unarchived_measurements)
    dT = dT.total_seconds()
    for key in ["power", "voltage", "current"]:
        power = 0.0
        for umeasurement in unarchived_measurements:
            try:
                power += getattr(umeasurement, key) * dT
            except (AttributeError, TypeError) as e:
                pass

        try:
            setattr(measurement, key, power)
        except KeyError:
            pass

    # Phase????
    # TODO: Figure this out.
    measurement.phase = unarchived_measurements.first().phase

    measurement.save()
    unarchived_measurements.delete()

def convert_measurement_value(value, circuit, key):
    if key == "voltage":
        value = value / 16
        ct_type = circuit.circuit_transformer_type
        ct_equation_voltage = settings.CT_VOLTAGE[ct_type]
        return value * ct_equation_voltage[0] + ct_equation_voltage[1]
    elif key == "current":
        value = value / 16
        ct_type = circuit.circuit_transformer_type
        ct_equation_voltage = settings.CT_VOLTAGE[ct_type]
        ct_equation_current = settings.CT_CURRENT[ct_type]
        voltage = value * ct_equation_voltage[0] + ct_equation_voltage[1]
        return voltage * ct_equation_current[0] + ct_equation_current[1]
    else:
        # Phase eventually needs to be converted as well.
        return value
