from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
	path('', views.Dashboard.as_view(), name="dashboard"),
	path('mahila-pratinidhi-forms-list/<district_id>', views.MahilaPratinidhiDashboardView.as_view(), name="mahila_pratinidhi_form_dashboard"),
	path('mahila-pratinidhi-form/<district_id>', views.MahilaPratinidhiFormCreateView.as_view(), name="mahila_pratinidhi_form"),
	path('mahila-pratinidhi-detail/<int:pk>/', views.MahilaPratinidhiFormDetailView.as_view(), name="mahila_pratinidhi_detail"),
	path('mahila-pratinidhi-update/<int:pk>/', views.MahilaPratinidhiFormUpdateView.as_view(), name="mahila_pratinidhi_update"),
	path('mahila-pratinidhi-delete/<int:pk>/', views.MahilaPratinidhiFormDeleteView.as_view(), name="mahila_pratinidhi_delete"),
	path('file-upload/', views.file_upload, name="file_upload"),

]