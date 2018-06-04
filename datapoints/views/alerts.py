import json
import logging

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from datapoints.models import Alert, Circuit


def get_all_alerts_or_add_alert(request):
    logger = logging.getLogger(__name__)
    logger.info(request.method)
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        logger.info(body)
        # Create new alert
        alert = Alert()
        # Get the circuit for the
        circuit = get_object_or_404(Circuit, id=getattr(body, "circuit"))
        alert.circuit = circuit
        del body.circuit

        for key, value in body.items():
            setattr(alert, key, value)
        alert.save()
        return JsonResponse({"status": "success"})
    else:
        # Return all alerts
        alerts = Alert.objects.all()
        return HttpResponse(serializers.serialize('json', alerts))

def edit_alert(request, id):
    pass
