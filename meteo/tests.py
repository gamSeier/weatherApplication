from datetime import datetime as dt
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class TempHereViewTests(TestCase):
    @patch('meteo.views.datetime')
    @patch('meteo.views.requests.get')
    @patch('meteo.views.geocoder.ip')
    def test_timezone_auto_in_api_request(self, mock_geocoder_ip, mock_requests_get, mock_datetime):
        mock_geocoder_ip.return_value.latlng = (0.0, 0.0)
        mock_datetime.now.return_value = dt(2024, 1, 1, 5, 0, 0)
        mock_requests_get.return_value.json.return_value = {
            'hourly': {'temperature_2m': list(range(24))}
        }

        response = self.client.get(reverse('temp_here'))

        self.assertEqual(response.status_code, 200)
        args, kwargs = mock_requests_get.call_args
        self.assertEqual(kwargs['params']['timezone'], 'auto')
        self.assertIn('<h2>5&#8457;</h2>', response.content.decode())
