from django.test import TestCase
from django.urls import reverse

from siedlungsmanager.models import Siedlung


class SiedlungFormTestCase(TestCase):
    def setUp(self):
        # Create a test Siedlung
        self.siedlung = Siedlung.objects.create(
            internal_id='TEST',
            bezeichnung='Test Siedlung',
            anlagewert=100000,
            versicherungswert=110000,
            baurechtszins=5000,
            betriebsquote_zuschlag=0
        )

    def test_invalid_betriebsquote_upper_bound(self):
        # Assuming you have a view named 'my_form' that handles the form
        url = reverse('siedlung_update', kwargs={'siedlung_pk': self.siedlung.pk})

        # Prepare invalid data
        invalid_data = {
            'betriebsquote_zuschlag': '100.1',
            # Add other form fields as needed
        }

        # Send a POST request with invalid data
        response = self.client.post(url, data=invalid_data)

        # Check if the response contains an error message
        self.assertContains(response, 'Der Wert muss zwischen 0 und 100 liegen')

    def test_invalid_betriebsquote_lower_bound(self):
        url = reverse('siedlung_update', kwargs={'siedlung_pk': self.siedlung.pk})

        # Prepare invalid data
        invalid_data = {
            'betriebsquote_zuschlag': '-1',
            # Add other form fields as needed
        }

        # Send a POST request with invalid data
        response = self.client.post(url, data=invalid_data)

        # Check if the response contains an error message
        self.assertContains(response, 'zwischen 0 und 100')

    def test_invalid_betriebsquote_decimal(self):
        # Assuming you have a view named 'my_form' that handles the form
        url = reverse('siedlung_update', kwargs={'siedlung_pk': self.siedlung.pk})

        # Prepare invalid data
        invalid_data = {
            'betriebsquote_zuschlag': '5.125',
            # Add other form fields as needed
        }

        # Send a POST request with invalid data
        response = self.client.post(url, data=invalid_data)

        # Check if the response contains an error message
        self.assertContains(response, 'höchstens 2 Dezimalstellen')




