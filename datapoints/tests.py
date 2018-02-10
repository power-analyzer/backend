import json
from django.test import TestCase, Client
from django.urls import reverse
from datapoints.models import Device


class GenericTest(TestCase):

    def test_did_compile(self):
        client = Client()
        response = client.get(reverse('datapoints:index'))
        self.assertIs(response.status_code, 200)

    def test_batch_upload(self):
        client = Client()
        device = Device()
        device.save()
        measurements = json.dumps({"measurements": [
            {"circuit_id": 1, "voltage": 120, "current": 10, "phase": 0},
            {"circuit_id": 2, "power": 456, "current": 45645, "phase": 456.35}
        ]})
        response = client.post(
            reverse("datapoints:batch_upload",
                    kwargs={'device_id': device.id}),
            data=str(measurements),
            content_type="text/html"
        )
        self.assertIs(response.status_code, 200)
