from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib import admin
# from public.views import NameAutocomplete



app_name = 'public'


urlpatterns = [
	path('', views.Index.as_view(), name="index"),
	path('signup/', views.signup, name="signup"),
	path('activate/<uidb64>/<token>', views.activate, name='activate'),


	path('explore/<slug:clicked>', views.ExploreView.as_view(), name="explore"),
	path('explore/district/<district_id>/', views.MahilaPratinidhiView.as_view(), name="explore_district"),
	path('explore/district/<district_id>/<int:pk>/', views.LocalMahilaPratinidhiDetail.as_view(),
	name="local_mahila_detail"),
	path('read/', views.read_view, name="read"),
	path('explore/<explore_province>/', views.ProvinceView.as_view(), name="explore_province"),

	path('explore/province/<province_id>/', views.ProvinceView.as_view(), name="explore_province"),
	# path(r'^explore/province/<province_id>/(?P<party>\w+)/$', views.ProvinceView.as_view),
	path('explore/province/<province_id>/<int:pk>/', views.ProvincialMahilaPratinidhiDetail.as_view(),
	name="provincial_mahila_detail"),

	path('detail/<int:pk>', views.MahilaDetail.as_view(), name="detail"),
	path('detail/national/<int:pk>/', views.RastriyaMahilaDetail.as_view(), name="national_detail"),
	path('detail/pratinidhi/<int:pk>', views.PratinidhiMahilaDetail.as_view(), name="pratinidhi_detail"),
	path('detail/pratinidhi/<int:pk>/call', views.callRequestView, name="pratinidhi_call_request"),

	path('visualize/', views.DataVisualize.as_view(), name="data_visualize"),
	path('visualize/<variable>/<key>',views.VisualizeIndividual.as_view(),name="visualize_individual"),
	path('map',views.MapVisualize.as_view(),name="map_visualize"),

	path('news/<int:pk>/', views.NewsView.as_view(), name="news"),

	# path(r'^detail/name/(?P<name>\w+)/$', views.SearchDetail.as_view(), name='name_search'),

	# path(r'^name-autocomplete/$', NameAutocomplete.as_view(), name="name-autocomplete"),
]
