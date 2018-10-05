from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
	path('', views.MainDashboard.as_view(), name="main_dashboard"),

	path('rastriya-shava-forms-list/', views.RastriyaShavaDashboardView.as_view(), name="rastriya_shava_form_dashboard"),
	path('rastriya-shava-form/', views.RastriyaShavaCreateView.as_view(), name="rastriya_shava_form"),
	path('rastriya-shava-detail/<int:pk>/', views.RastriyaShavaDetailView.as_view(), name="rastriya_shava_detail"),
	path('rastriya-shava-update/<int:pk>/', views.RastriyaShavaUpdateView.as_view(), name="rastriya_shava_update"),
	path('rastriya-shava-delete/<int:pk>/', views.RastriyaShavaDeleteView.as_view(), name="rastriya_shava_delete"),
	path('rastriya-shava-upload/', views.UloadView.as_view(), name="rastriya_shava_upload"),
	path('rastriya-shava-file-upload/', views.file_upload, name="rastriya_shava_file_upload"),

	path('district-dashboard/', views.Dashboard.as_view(), name="dashboard"),
	path('mahila-pratinidhi-forms-list/<district_id>', views.MahilaPratinidhiDashboardView.as_view(), name="mahila_pratinidhi_form_dashboard"),
	path('mahila-pratinidhi-form/<district_id>', views.MahilaPratinidhiFormCreateView.as_view(), name="mahila_pratinidhi_form"),
	path('mahila-pratinidhi-detail/<int:pk>/', views.MahilaPratinidhiFormDetailView.as_view(), name="mahila_pratinidhi_detail"),
	path('mahila-pratinidhi-update/<int:pk>/', views.MahilaPratinidhiFormUpdateView.as_view(), name="mahila_pratinidhi_update"),
	path('mahila-pratinidhi-delete/<int:pk>/', views.MahilaPratinidhiFormDeleteView.as_view(), name="mahila_pratinidhi_delete"),
	path('upload/', views.UloadView.as_view(), name="upload"),
	path('file-upload/', views.file_upload, name="file_upload"),

	path('province-dashboard/', views.ProvinceDashboard.as_view(), name="province_dashboard"),
	path('province-mahila-pratinidhi-forms-list/<province_id>', views.ProvinceMahilaPratinidhiDashboardView.as_view(), name="province_mahila_pratinidhi_form_dashboard"),
	path('province-mahila-pratinidhi-form/<province_id>', views.ProvinceMahilaPratinidhiFormCreateView.as_view(), name="province_mahila_pratinidhi_form"),
	path('province-mahila-pratinidhi-detail/<int:pk>/', views.ProvinceMahilaPratinidhiFormDetailView.as_view(), name="province_mahila_pratinidhi_detail"),
	path('province-mahila-pratinidhi-update/<int:pk>/', views.ProvinceMahilaPratinidhiFormUpdateView.as_view(), name="province_mahila_pratinidhi_update"),
	path('province-mahila-pratinidhi-delete/<int:pk>/', views.ProvinceMahilaPratinidhiFormDeleteView.as_view(), name="province_mahila_pratinidhi_delete"),
	path('province-upload/', views.ProvinceUloadView.as_view(), name="province_upload"),
	path('province-file-upload/', views.province_file_upload, name="province_file_upload"),

	path('accounts/user-profile/<int:pk>', views.UserProfileView.as_view(), name='user_profile'),
	path('accounts/user-profile-update/<int:pk>', views.UserProfileUpdateView.as_view(), name='user_profile_update'),
]