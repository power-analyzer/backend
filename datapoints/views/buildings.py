import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone
# from django.shortcuts import get_object_or_404

from datapoints.models import UnarchivedMeasurement
from datapoints.utilities import get_or_add_device, archive_or_add_measurement, convert_measurement_value


def get_buildings(request):
    return HttpResponse("Getting a list of buildings...")

def get_building(request, id):
    return HttpResponse("Getting that building...")
