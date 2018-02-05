import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from .models import Measurement, Circuit


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
