from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView

from .models import MahilaPratinidhiForm, District, BOOL_CHOICES
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

	def get_context_data(self, **kwargs):
		context = super(MahilaPratinidhiFormCreateView, self).get_context_data(**kwargs)
		context['district'] = District.objects.get(id=self.kwargs['district_id'])
		return context


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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['district'] = self.object.district
		return context


class MahilaPratinidhiFormUpdateView(LoginRequiredMixin, UpdateView):

	model = MahilaPratinidhiForm
	form_class = MahilaPratinidhiFormForm
	success_url = reverse_lazy('core:dashboard')
	template_name = "core/mahila_pratinidhi_form.html"

	def get_success_url(self):
		success_url = reverse_lazy('core:mahila_pratinidhi_form_dashboard', args=(self.object.district.pk,))
		return success_url

	def get_context_data(self, **kwargs):
		context = super(MahilaPratinidhiFormUpdateView, self).get_context_data(**kwargs)
		context['district'] = MahilaPratinidhiForm.objects.get(id=self.kwargs['pk']).district
		context['is_update_form'] = True
		return context


class MahilaPratinidhiFormDeleteView(LoginRequiredMixin, DeleteView):

	model = MahilaPratinidhiForm
	template_name = "core/mahila_pratinidhi_delete.html"
	context_object_name = 'form'

	def get_success_url(self):
		success_url = reverse_lazy('core:mahila_pratinidhi_form_dashboard', args=(self.object.district.pk,))
		return success_url

	def get_context_data(self, **kwargs):
		context = super(MahilaPratinidhiFormDeleteView, self).get_context_data(**kwargs)
		context['district'] = self.object.district
		return context


def file_upload(request):
	import pandas as pd
	df = pd.read_excel(request.FILES['sentFile'])
	# paramFile = request.FILES['sentFile'].read()
	print(df.columns)


class MahilaPratinidhiDashboardView(LoginRequiredMixin, TemplateView):
	template_name = 'core/mahila_pratinidhi_dashboard.html'

	def get(self, request, *args, **kwargs):
		forms = MahilaPratinidhiForm.objects.filter(district_id=self.kwargs.get('district_id'))
		status = self.request.GET.get('status')
		district_id = self.kwargs.get('district_id')
		district = District.objects.get(id=district_id)
		status_choices = BOOL_CHOICES
		if status:
			forms = MahilaPratinidhiForm.objects.filter(district_id=self.kwargs.get('district_id'), status=status)
		return render(request, self.template_name, {'forms': forms, 'district_id': district_id, 'status_choices': status_choices, 'district': district})
