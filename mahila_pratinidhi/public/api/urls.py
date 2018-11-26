from django.urls import path, include
from rest_framework import routers

from . import viewset


urlpatterns = [
	path('geojson/country/', viewset.country_geojson),
	path('geojson/province/<province_id>/', viewset.province_geojson),
	path('geojson/municipality/<district>/', viewset.gapanapa_geojson),

	path('country/', viewset.RastriyaViewSet.as_view({'get': 'list'})),
	path('age/', viewset.AgeViewSet.as_view()),
	path('ethnicity/', viewset.EthnicityViewSet.as_view()),
	path('mother_tongue/', viewset.MotherTongueViewSet.as_view()),
	path('education/', viewset.EducationViewSet.as_view()),
]