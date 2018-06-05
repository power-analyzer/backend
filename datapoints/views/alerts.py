import json

from django.core import serializers
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from datapoints.models import Alert, Circuit

@require_http_methods(["GET", "POST"])
def get_all_alerts_or_add_alert(request):
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

        alert.last_used = timezone.make_aware(timezone.datetime.min, timezone.get_default_timezone())
        alert.save()
        # Litterally the ugliest serialization ever.
        json_alert = serializers.serialize('json', [alert])
        json_alert = json.loads(json_alert)[0]
        return JsonResponse({"status": "success", "alert": json_alert})
    else:
        # Return all alerts
        alerts = Alert.objects.all()
        return HttpResponse(serializers.serialize('json', alerts))

@require_http_methods(["POST", "DELETE"])
def edit_alert(request, id):
    if request.method == "POST":
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
    else:
        alert = get_object_or_404(Alert, id=id)
        alert.delete()
    return JsonResponse({"status": "success"})
