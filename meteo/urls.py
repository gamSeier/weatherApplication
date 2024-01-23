from django.urls import path

from meteo import views


urlpatterns = [
    path('meteo/', views.temp_here, name='temp_here')
]