import geocoder
import requests
from datetime import datetime

from django.http import HttpResponse
from django.template import loader


def temp_here(request):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    location = geocoder.ip('me').latlng
    params = {
        "latitude": location[0],
        "longitude": location[1],
        "hourly": "temperature_2m",
        "temperature_unit": "fahrenheit",
        "timezone": "auto",
    }
    now = datetime.now()
    hour = now.hour
    meteo_data = requests.get(endpoint, params=params).json()
    temp = meteo_data['hourly']['temperature_2m'][hour]
    template = loader.get_template('index.html')
    context = {'temp': temp}
    return HttpResponse(template.render(context, request))
