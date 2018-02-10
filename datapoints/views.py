import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
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
            try:
                setattr(measurement, key, reading[key])
            except KeyError:
                pass

        measurement.circuit = circuit
        measurement.save()
    return HttpResponse('{status:"success"}')


@require_GET
def register_device(request):
    new_device = Device()
    new_device.save()
    new_device.name = "New Device " + str(new_device.id)
    new_device.save()
    return JsonResponse({"device_id": new_device.id})
