from django.urls import path, include
from rest_framework import routers

from . import viewset


urlpatterns = [
	path('geojson/country/', viewset.country_geojson),
	path('geojson/province/<province_id>/', viewset.province_geojson),
	path('geojson/municipality/<district>/', viewset.gapanapa_geojson),


]