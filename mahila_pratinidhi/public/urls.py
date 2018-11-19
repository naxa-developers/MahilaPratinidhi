from django.urls import path, re_path
from django.conf.urls import url
from . import views


app_name = 'public'


urlpatterns = [
	path('', views.Index.as_view(), name="index"),
	path('signup/', views.signup, name="signup"),
	# re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
	path('activate/<uidb64>/<token>', views.activate, name='activate'),
	
	
	path('explore/', views.ExploreView.as_view(), name="explore"),
	path('explore/<district_id>/', views.MahilaPratinidhiView.as_view(), name="explore_district"),
	path('explore/<explore_province>/', views.ProvinceView.as_view(), name="explore_province"),
	
	path('detail/<int:pk>/', views.Detail.as_view(), name="mahila_detail"),

	path('visualize/', views.DataVisualize.as_view(), name="data_visualize"),
	path('tab/', views.Tab.as_view(), name="tab"),
]