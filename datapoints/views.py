import json

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
# from django.shortcuts import get_object_or_404

from .models import Measurement
from .utilities import get_or_add_device


def index(request):
    return HttpResponse("Hello")


@require_POST
def batch_upload(request, mac):
    device = get_or_add_device(mac)
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
    return HttpResponse('{"status":"success"}')


@require_GET
def register_device(request, mac):
    device = get_or_add_device(mac)
    return JsonResponse({"mac": device.mac})


@require_GET
def get_relative_circuit(request, device_id, circuit_id, start_time, end_time):
    try:
        device = Device.objects.get(pk=device_id)
        circuit = Circuit.objects.get(device=device, id=circuit_id)

    except MultipleObjectsReturned:
        return HttpResponseBadRequest({'status': 'success'})


@require_GET
def get_circuit(request, circuit_id):
    pass
