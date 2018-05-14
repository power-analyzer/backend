from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import timezone

from datapoints.models import Circuit, Measurement


def get_circuits(request):
    circuits = Circuit.objects.all()
    return HttpResponse(serializers.serialize('json', circuits))

def get_circuit(request, id):
    circuit = get_object_or_404(Circuit, id=id)
    return JsonResponse(model_to_dict(circuit))

def get_current_usage(request, end_date):
    now = timezone.now()
    return get_usage(request, end_date, now.isoformat())

def get_usage(request, end_date, start_date):
    # TODO: Implement this. :)
    # measurements = Measurement.objects.filter(date__range=[start_date, end_date])

    # return HttpResponse(serializers.serialize('json', measurements))
    return HttpResponse("hello")
