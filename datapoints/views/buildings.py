from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.forms.models import model_to_dict

from datapoints.models import Building


def get_buildings(request):
    buildings = Building.objects.all()
    return HttpResponse(serializers.serialize('json', buildings))

def get_building(request, id):
    building = get_object_or_404(Building, id=id)
    return JsonResponse(model_to_dict(building))

def get_usage(request):
    # TODO: Implement this. :)
    return HttpResponse("To be implemented")
