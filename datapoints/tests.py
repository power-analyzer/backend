import json
from django.test import TestCase, Client
from django.urls import reverse
from datapoints.models import Device, UnarchivedMeasurement


class GenericTest(TestCase):

    def test_did_compile(self):
        client = Client()
        response = client.get(reverse('datapoints:index'))
        self.assertIs(response.status_code, 200)

    def test_batch_upload(self):
        test_mac = "123456"
        client = Client()
        device = Device()
        device.mac = test_mac
        device.save()
        measurements = json.dumps({"measurements": [
            {"circuit_id": 1, "voltage": 120, "current": 10, "phase": 0},
            {"circuit_id": 2, "power": 456, "current": 45645, "phase": 456.35}
        ]})
        response = client.post(
            reverse("datapoints:batch_upload",
                    kwargs={'mac': test_mac}),
            data=str(measurements),
            content_type="text/html"
        )
        self.assertIs(response.status_code, 200)


    def test_archive_measurements(self):
        # TODO: Write this
        pass
