import json
import logging

from django.core import serializers
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse

from datapoints.models import Alert, Circuit

@require_http_methods(["GET", "POST"])
def get_all_alerts_or_add_alert(request):
    logger.info(request.method)
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # Create new alert
        alert = Alert()
        # Get the circuit for the
        circuit = get_object_or_404(Circuit, id=body["circuit"])
        alert.circuit = circuit
        del body["circuit"]

        for key, value in body.items():
            setattr(alert, key, value)
        alert.save()
        return JsonResponse({"status": "success"})
    else:
        # Return all alerts
        alerts = Alert.objects.all()
        return HttpResponse(serializers.serialize('json', alerts))

@require_http_methods(["POST"])
def edit_alert(request, id):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # Create new alert
    alert = get_object_or_404(Alert, id=id)
    # Get the circuit for the
    circuit = get_object_or_404(Circuit, id=body["circuit"])
    alert.circuit = circuit
    del body["circuit"]

    for key, value in body.items():
        setattr(alert, key, value)
    alert.save()
    return JsonResponse({"status": "success"})
