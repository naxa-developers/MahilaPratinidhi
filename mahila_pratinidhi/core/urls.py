from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('mahila-pratinidhi-form/', views.MahilaPratinidhiFormCreateView.as_view(), name="mahila_pratinidhi_form"),
	path('', views.MahilaPratinidhiFormListView.as_view(),name="mahila_pratinidhi_list"),
	path('mahila-pratinidhi-detail/<int:pk>/', views.MahilaPratinidhiFormDetailView.as_view(), name="mahila_pratinidhi_detail"),
	path('mahila-pratinidhi-update/<int:pk>/', views.MahilaPratinidhiFormUpdateView.as_view(), name="mahila_pratinidhi_update"),
	path('mahila-pratinidhi-delete/<int:pk>/', views.MahilaPratinidhiFormDeleteView.as_view(), name="mahila_pratinidhi_delete"),

]

