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

    # TODO: Change this to just average phase and magnitude of data.
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

# def convert_measurement_value(value, circuit, key):
#     if key == "voltage":
#         value = value / 16
#         ct_type = circuit.circuit_transformer_type
#         ct_equation_voltage = settings.CT_VOLTAGE[ct_type]
#         return value * ct_equation_voltage[0] + ct_equation_voltage[1]
#     elif key == "current":
#         value = value / 16
#         ct_type = circuit.circuit_transformer_type
#         ct_equation_voltage = settings.CT_VOLTAGE[ct_type]
#         ct_equation_current = settings.CT_CURRENT[ct_type]
#         voltage = value * ct_equation_voltage[0] + ct_equation_voltage[1]
#         return voltage * ct_equation_current[0] + ct_equation_current[1]
#     else:
#         # Phase eventually needs to be converted as well.
#         return value


def convert_voltage_measurements(voltages):
    Vmax = max(voltages)
    Vmin = min(voltages)
    offset = (Vmin + Vmax)/2.0

    np_voltages = np.array(voltages)
    Vin = settings.V_IN

    translated_v = ((np_voltages/Vin["num_bits"])*Vin["max_val"]-offset)/Vin["scale_factor"]

    fft = np.fft.fft(translated_v)

    # TODO: Generalize this for better results
    return fft[33]



def convert_current_measurements(currents):
    Imax = max(currents)
    Imin = min(currents)
    offset = (Imin + Imax) / 2

    np_currents = np.array(currents)
    Iin = settings.I_IN

    translated_i = ((np_currents/Iin["num_bits"])*Iin["max_val"] - offset)/Iin["scale_factor"]*Iin["secondary"]

    fft = np.fft.fft(translated_i)

    # TODO: Generalize this for better results
    return fft[33]


def calculate_complex_power(voltage, current):
    complex_power =  voltage * current
    rms_power = complex_power / math.sqrt(2)
    return cmath.polar(rms_power)
