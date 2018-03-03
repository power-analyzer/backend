import json
import random

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from datapoints.models import Device, UnarchivedMeasurement, Measurement
from datapoints.utilities import archive_or_add_measurement, convert_measurement_value


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


    def populate_measurement(self, measurement, circuit, time=None):
        if time == None:
            time = timezone.now()
        measurement.time = time
        measurement.circuit = circuit
        for key in ["current", "voltage", "phase"]:
            setattr(measurement, key, random.randint(1,10)*5)


    def test_archive_measurements(self):
        device = Device()
        device.mac = "test_archive_measurements() mac"
        device.name = "test"
        device.location = "N/A"
        device.description = "test device for test_archive_measurements()"
        device.save()

        circuit = device.add_or_get_circuit_id(0)

        old = UnarchivedMeasurement()
        mid = UnarchivedMeasurement()
        new = UnarchivedMeasurement()

        now = timezone.now()
        self.populate_measurement(old, circuit, now)
        self.populate_measurement(mid, circuit, now + timezone.timedelta(minutes=15))
        self.populate_measurement(new, circuit, now + timezone.timedelta(minutes=settings.ARCHIVE_TIME + 1))

        archive_or_add_measurement(old)
        archive_or_add_measurement(mid)
        self.assertIs(len(UnarchivedMeasurement.objects.filter(circuit=circuit)), 2, msg="archive_or_add_measurement() didn't insert measurement")
        archive_or_add_measurement(new)
        self.assertIs(len(UnarchivedMeasurement.objects.filter(circuit=circuit)), 1, msg="archive_or_add_measurement() didn't archive measurements")
        self.assertIs(len(Measurement.objects.filter(circuit=circuit)), 1, msg="archive_measurements() didnt' add a new Measurement()")

    def test_convert_measurement_value(self):
        device = Device()
        device.mac = "test_convert_measurement_value Mac"
        device.name = "test"
        device.location = "N/A"
        device.description = "test device"
        device.save()

        circuit = device.add_or_get_circuit_id(0)

        test1 = convert_measurement_value(1000, circuit, "voltage")
        self.assertAlmostEqual(test1, 0.1972, "Problem with voltage calculation in test_convert_measurement_value")

        test2 = convert_measurement_value(1000, circuit, "current")
        self.assertAlmostEqual(test2, 8.992688, "Problem with current calculation in test_convert_measurement_value")
