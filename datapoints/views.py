import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from .models import Measurement, Circuit, Device


def index(request):
    return HttpResponse("Hello")


@require_POST
def upload(request, device_id, circuit_id):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    circuit = get_object_or_404(Circuit, pk=circuit_id)
    measurement = Measurement()
    measurement.power = body["power"]
    measurement.circuit = circuit
    measurement.save()
    return HttpResponse('{status:"success"}')


@require_POST
def batch_upload(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    measurements = body["measurements"]
    for reading in measurements:
        # Get circuit
        circuit = device.add_or_get_circuit_id(reading["circuit_id"])
        # Set Measurement
        measurement = Measurement()
        for key in ["power", "voltage", "current", "phase"]:
            setattr(measurement, key, reading[key])
            # measurement[key] = reading[key]
        # measurement["power"] = reading["power"]
        # measurement.voltage = reading["voltage"]
        # measurement.current = reading["current"]
        # measurement.phase = reading["phase"]
        measurement.circuit = circuit
        measurement.save()
    return HttpResponse('{status:"success"}')
