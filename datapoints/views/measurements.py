import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone
# from django.shortcuts import get_object_or_404

from datapoints.models import UnarchivedMeasurement
from datapoints.utilities.measurements import (
        get_or_add_device,
        archive_or_add_measurement,
        convert_voltage_measurements,
        convert_current_measurements,
        calculate_complex_power,
    )
from datapoints.utilities.email import check_alert


def index(request):
    return HttpResponse("Hello")


@require_POST
def batch_upload(request, mac):
    device = get_or_add_device(mac)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    voltages = body["V"]
    del body["V"]
    complex_voltage = convert_voltage_measurements(voltages)

    time = timezone.now()
    for circuit_id, readings in body.items():
        # Get circuit
        circuit = device.add_or_get_circuit_id(int(circuit_id))
        # create a new Measurement() and the values for it
        measurement = UnarchivedMeasurement()
        measurement.time = time
        complex_current = convert_current_measurements(readings)
        magnitude, phase = calculate_complex_power(complex_voltage, complex_current)
        measurement.magnitude = magnitude
        measurement.phase = phase
        measurement.circuit = circuit
        check_alert(circuit, measurement)
        archive_or_add_measurement(measurement)
    return HttpResponse('{"status":"success"}')


@require_GET
def register_device(request, mac):
    device = get_or_add_device(mac)
    return JsonResponse({"mac": device.mac})
