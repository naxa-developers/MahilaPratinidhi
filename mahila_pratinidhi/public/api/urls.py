from django.urls import path, include
from rest_framework import routers

from . import viewset


urlpatterns = [
	path('geojson/country/', viewset.country_geojson),
	path('geojson/districts',viewset.districts_geojson),
	path('geojson/province/<province_id>/', viewset.province_geojson),
	path('geojson/municipality/<district>/', viewset.gapanapa_geojson),
	path('geojson/municipality/', viewset.municipality_geojson),

	path('hlcit/<hlcit>', viewset.HlcitViewSet.as_view({'get':'list'})),
	path('country/', viewset.RastriyaViewSet.as_view({'get': 'list'})),
	path('maps/', viewset.MapViewSet.as_view()),
	path('age/', viewset.AgeViewSet.as_view()),
	path('age/local/', viewset.LocalAgeViewSet.as_view()),
	path('age/national/', viewset.NationalAgeViewSet.as_view()),
	path('age/federal/', viewset.FederalAgeViewSet.as_view()),
	path('age/province/', viewset.ProvinceAgeViewSet.as_view()),
	path('ethnicity/', viewset.EthnicityViewSet.as_view()),
	path('mother_tongue/', viewset.MotherTongueViewSet.as_view()),
	path('education/', viewset.EducationViewSet.as_view()),
	path('political_engagement/', viewset.PoliticalEngagementViewSet.as_view()),
	path('election_type/', viewset.ElectionTypeViewSet.as_view()),
	path('marital_status/', viewset.MaritalStatusViewSet.as_view()),
	path('election_experience/', viewset.ElectionParticipate.as_view()),
	path('party/', viewset.PartyViewSet.as_view()),
	path('political_commitment/', viewset.CommitmentViewSet.as_view()),

	path('districts/', viewset.DistrictsViewSet.as_view({'get': 'list'})),
	path('municipalities/',viewset.MunicipalityViewSet.as_view({'get':'list'})),
	path('all/<hlcit1>/<hlcit2>', viewset.CompareAllViewSet.as_view()),
	path('province/<province1>/<province2>', viewset.CompareProvinceViewSet.as_view()),
	path('district/<district1>/<district2>', viewset.CompareDistrictViewSet.as_view()),
	path('pie/', viewset.PieChartViewSet.as_view()),
]
