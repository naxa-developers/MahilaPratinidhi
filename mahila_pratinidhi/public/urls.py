from django.urls import path, re_path
from django.conf.urls import url
from . import views


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
	path('explore/province/<province_id>/<int:pk>/', views.ProvincialMahilaPratinidhiDetail.as_view(),
	name="provincial_mahila_detail"),

	
	path('detail/national/<int:pk>/', views.RastriyaMahilaDetail.as_view(), name="national_detail"),
	path('detail/pratinidhi/<int:pk>', views.PratinidhiMahilaDetail.as_view(), name="pratinidhi_detail"),

	path('visualize/', views.DataVisualize.as_view(), name="data_visualize"),
]