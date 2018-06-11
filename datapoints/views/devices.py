from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.forms.models import model_to_dict

from datapoints.models import Device, Circuit


def get_devices(request):
    devices = Device.objects.all()
    return HttpResponse(serializers.serialize('json', devices))

def get_device_circuits(request, id):
    circuits = Circuit.objects.filter(device=id);
    return HttpResponse(serializers.serialize('json', circuits))

def get_device(request, id):
    device = get_object_or_404(Device, id=id)
    return JsonResponse(model_to_dict(device))

def get_usage(request):
    # TODO: Implement this. :)
    return HttpResponse("To be implemented")
