from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView

from .models import MahilaPratinidhiForm, District
from .forms import MahilaPratinidhiFormForm


class MahilaPratinidhiFormCreateView(LoginRequiredMixin, CreateView):

	model = MahilaPratinidhiForm
	form_class = MahilaPratinidhiFormForm
	template_name = "core/mahila_pratinidhi_form.html"

	def form_valid(self, form):
		form.instance.district = get_object_or_404(District, pk=self.kwargs['district_id'])
		return super().form_valid(form)

	def get_success_url(self):
		success_url = reverse_lazy('core:mahila_pratinidhi_form_dashboard', args=(self.kwargs.get('district_id'),))
		return success_url


class Dashboard(LoginRequiredMixin, TemplateView):

	template_name = "core/dashboard.html"

	def get(self, request, *args, **kwargs):
		districts = District.objects.all()
		district = request.GET.get('dist')
		district = District.objects.filter(name=district)

		return render(request, self.template_name, {'districts': districts, 'district': district})


class MahilaPratinidhiFormDetailView(LoginRequiredMixin, DetailView):

	model = MahilaPratinidhiForm
	template_name = "core/mahila_pratinidhi_detail.html"
	context_object_name = 'form'


class MahilaPratinidhiFormUpdateView(LoginRequiredMixin, UpdateView):

	model = MahilaPratinidhiForm
	form_class = MahilaPratinidhiFormForm
	success_url = reverse_lazy('core:dashboard')
	template_name = "core/mahila_pratinidhi_form.html"

	def get_success_url(self):
		success_url = reverse_lazy('core:mahila_pratinidhi_form_dashboard', args=(self.object.district.pk,))
		return success_url


class MahilaPratinidhiFormDeleteView(LoginRequiredMixin, DeleteView):

	model = MahilaPratinidhiForm
	template_name = "core/mahila_pratinidhi_delete.html"

	def get_success_url(self):
		success_url = reverse_lazy('core:mahila_pratinidhi_form_dashboard', args=(self.object.district.pk,))
		return success_url


def file_upload(request):
	import pandas as pd
	df = pd.read_excel(request.FILES['sentFile'])
	# paramFile = request.FILES['sentFile'].read()
	print(df.columns)


class MahilaPratinidhiDashboardView(LoginRequiredMixin, TemplateView):
	template_name = 'core/mahila_pratinidhi_dashboard.html'

	def get(self, request, *args, **kwargs):
		district_id = self.kwargs.get('district_id')
		forms = MahilaPratinidhiForm.objects.filter(district_id=self.kwargs.get('district_id'))
		return render(request, self.template_name, {'forms': forms, 'district_id': district_id})
