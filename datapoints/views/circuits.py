from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import timezone, dateparse

from datapoints.models import Circuit, Measurement


def get_circuits(request):
    circuits = Circuit.objects.all()
    return HttpResponse(serializers.serialize('json', circuits))


def get_circuit(request, id):
    circuit = get_object_or_404(Circuit, id=id)
    return JsonResponse(model_to_dict(circuit))


def get_current_usage(request, id, end_date):
    now = timezone.now()
    return get_usage(request, id, end_date, now.isoformat())


def get_usage(request, id, end_date, start_date):
    start = dateparse.parse_datetime(start_date)
    end = dateparse.parse_datetime(end_date)

    measurements = Measurement.objects.filter(circuit=id)
    measurements = measurements.filter(time__gte=end, time__lte=start).order_by('time')

    # TODO: Implement some sort of "compression" so that if two years of data
    # is requested, there are only k number of "measurements" that accurately
    # measure the usage.
    # https://docs.djangoproject.com/en/2.0/ref/models/querysets/#aggregate
    # return HttpResponse(serializers.serialize('json', measurements))

    voltage = list(measurements.values_list('voltage', flat=True))
    labels = list(measurements.values_list('time', flat=True))

    return JsonResponse({"data": voltage, "labels": labels}, safe=False)
