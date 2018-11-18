from django.urls import path
from . import views


app_name = 'public'


urlpatterns = [
	path('', views.Index.as_view(), name="index"),
	path('signup/', views.SignUp.as_view(), name="signup"),
	
	
	path('explore/', views.ExploreView.as_view(), name="explore"),
	path('explore/<district_id>/', views.MahilaPratinidhiView.as_view(), name="explore_district"),
	path('explore/<explore_province>/', views.ProvinceView.as_view(), name="explore_province"),
	
	path('detail/<int:pk>/', views.Detail.as_view(), name="mahila_detail"),

	path('visualize/', views.DataVisualize.as_view(), name="data_visualize"),
	path('tab/', views.Tab.as_view(), name="tab"),
]