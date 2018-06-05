import json
import random

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from datapoints.models import Device, UnarchivedMeasurement, Measurement, Alert, Circuit
from datapoints.utilities.measurements import archive_or_add_measurement
from datapoints.utilities.email import check_alert

TEST_NUM_MAX = 50
TEST_NUM_MIN = 1

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
        measurements = json.dumps({"V":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],"1":[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],"2":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],"3":[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],"4":[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],"5":[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],"6":[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],"7":[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],"8":[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0,0,0],"9":[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],"10":[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],"11":[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],"12":[4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],"13":[4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],"14":[4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],"15":[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0]})
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
        for key in settings.MEASUREMENT_FIELDS:
            setattr(measurement, key, random.randint(TEST_NUM_MIN,TEST_NUM_MAX))


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

        new_measurements = Measurement.objects.filter(circuit=circuit)
        self.assertIs(len(new_measurements), 1, msg="archive_measurements() didnt' add a new Measurement()")
        for key in settings.MEASUREMENT_FIELDS:
            self.assertTrue(TEST_NUM_MIN <= getattr(new_measurements[0], key) <= TEST_NUM_MAX)

    def test_email(self):
        now = timezone.now()
        less_than_one_hour = now - timezone.timedelta(minutes=59)
        two_hours_ago = now - timezone.timedelta(hours=2)
        default = 20

        # Create Test Device & Circuit
        test_mac = "test_email"
        device = Device()
        device.mac = test_mac
        device.save()
        circuit = Circuit()
        circuit.device = device
        circuit.relative_id = 0

        circuit.save()

        #Create Test Alert
        alert = Alert()
        alert.circuit = circuit
        alert.last_used = two_hours_ago
        alert.frequency_limit = 1*60 #1hour*60min/hour
        alert.max_val = 30
        alert.min_val = 10
        alert.email = "ryan.rabello@wallawalla.edu"
        # alert.attribute = "magnitude" # This is default
        alert.save()

        #Create Measurement
        measurement = Measurement()
        measurement.circuit = circuit
        measurement.time = now
        measurement.magnitude = default
        measurement.phase = default
        measurement.max_p_phase = default
        measurement.max_i = default
        measurement.v_magnitude = default
        measurement.v_phase = default
        measurement.i_magnitude = default
        measurement.i_phase = default
        measurement.save()

        # Check to make sure no email is sent for value withing range.
        self.assertIs(check_alert(circuit, measurement), False, msg="check_alert() should not have sent an email")
        # Create low measurement
        alert.last_used = two_hours_ago
        alert.save()
        measurement.magnitude = 10
        measurement.save()
        self.assertIs(check_alert(circuit, measurement), True, msg="check_alert() should send an email (return True)")

        # Check High Measurement
        alert.last_used = two_hours_ago
        alert.save()
        measurement.magnitude = 30
        measurement.save()
        self.assertIs(check_alert(circuit, measurement), True, msg="check_alert() should send an email (return True)")

        # Check frequency_limit
        alert.last_used = less_than_one_hour
        alert.save()
        self.assertIs(check_alert(circuit, measurement), False, msg="check_alert() should not an email")
