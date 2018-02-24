import json
import datetime

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone
# from django.shortcuts import get_object_or_404

from .models import Measurement, UnarchivedMeasurement
from .utilities import get_or_add_device, archive_or_add_measurement


def index(request):
    return HttpResponse("Hello")


@require_POST
def batch_upload(request, mac):
    device = get_or_add_device(mac)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    measurements = body["measurements"]
    time = datetime.datetime.now()
    for reading in measurements:
        # Get circuit
        circuit = device.add_or_get_circuit_id(reading["circuit_id"])
        # Set Measurement
        measurement = UnarchivedMeasurement()
        measurement.time = time
        # TODO: Magic transformations.
        for key in ["power", "voltage", "current", "phase"]:
            try:
                setattr(measurement, key, reading[key])
            except KeyError:
                pass

        measurement.circuit = circuit
        archive_or_add_measurement(measurement)
    return HttpResponse('{"status":"success"}')


@require_GET
def register_device(request, mac):
    device = get_or_add_device(mac)
    return JsonResponse({"mac": device.mac})
