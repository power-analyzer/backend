from django.test import TestCase, Client
from django.urls import reverse


class GenericTest(TestCase):

    def test_did_compile(self):
        client = Client()
        response = client.get(reverse('datapoints:index'))
        self.assertIs(response.status_code, 200)
