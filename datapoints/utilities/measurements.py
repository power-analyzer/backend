import cmath
import math
import numpy as np

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
    for key in ["phase", "magnitude"]:

        sum_var = sum(map(lambda x: int(getattr(x, key)), unarchived_measurements))
        average = sum_var / len(unarchived_measurements)

        setattr(measurement, key, average)

    measurement.save()
    unarchived_measurements.delete()


def convert_voltage_measurements(voltages):
    np_voltages = np.array(voltages)
    Vin = settings.V_IN

    translated_v = (np_voltages/Vin["num_bits"])*Vin["max_val"]

    Vmax = max(translated_v)
    Vmin = min(translated_v)
    offset = (Vmin + Vmax)/2.0

    translated_v = (translated_v - offset)/Vin["scale_factor"]

    fft = np.fft.fft(translated_v)

    # TODO: Generalize this for better results
    return fft[33]



def convert_current_measurements(currents):
    np_currents = np.array(currents)
    Iin = settings.I_IN

    translated_i = (np_currents/Iin["num_bits"])*Iin["max_val"]
    Imax = max(translated_i)
    Imin = min(translated_i)
    offset = (Imin + Imax) / 2
    translated_i = (translated_i - offset)/Iin["scale_factor"]*Iin["secondary"]

    fft = np.fft.fft(translated_i)

    # TODO: Generalize this for better results
    return fft[33]


def calculate_complex_power(voltage, current):
    complex_power =  voltage * current
    rms_power = complex_power / math.sqrt(2)
    return cmath.polar(rms_power)
