from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
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


class UloadView(TemplateView):
	template_name = 'core/upload.html'

	def get_context_data(self, **kwargs):
		context = super(UloadView, self).get_context_data(**kwargs)
		context['districts'] = District.objects.all()
		return context


def file_upload(request):
	import pandas as pd

	try:

		request_files = request.FILES.getlist('file')
		files = [pd.read_excel(filename).fillna(value='') for filename in request_files]

		for df in files:
			total = df['qm=;+'].count()

			for row in range(0, total):
				print(request.POST.get('dist'))

				MahilaPratinidhiForm.objects.create(
					district=District.objects.get(name=request.POST.get('dist')),
					name=df['gfd'][row],
					age=df['pd]/'][row],
					marital_status=df['j}jflxs l:lYft'][row],
					educational_qualification=df['z}lIfs of]Uotf'][row],
					caste=df['hfltotf'][row],
					address=df['7]ufgf'][row],
					contact_number=df[';Dks{ g '][row],
					email=df['Od]n 7]ufgf'][row],
					nirwachit_padh=df['lgjf{lrt kb'][row],
					nirwachit_vdc_or_municipality_name=df['lgjf{lrt uf lj ; tyf gu/kflnsfsf]] gfd '][row],
					party_name=df['kf6L{sf] gfd '][row],
					party_joined_date=df['kf6L{df ;++++nUg ePsf] ldtL'][row],
					samlagna_sang_sastha_samuha=df[' ;++++nUg ;++3 ;F:yf ;d"x  '][row],
					nirwachit_chetra_pratiko_pratibadhata=df['lgjf{lrt Ifq k||ltsf] k|ltaM4tf '][row]
				)
		messages.success(request, 'Successfully loaded data from files')
		return HttpResponseRedirect('/upload')
	except:
		messages.error(request, "File Format not supported")
		return HttpResponseRedirect('/upload')


class MahilaPratinidhiDashboardView(LoginRequiredMixin, TemplateView):
	template_name = 'core/mahila_pratinidhi_dashboard.html'

	def get(self, request, *args, **kwargs):
		forms = MahilaPratinidhiForm.objects.filter(district_id=self.kwargs.get('district_id'))
		status = self.request.GET.get('status')
		district_id = self.kwargs.get('district_id')
		# district = District.objects.get(id=district_id)
		district = get_object_or_404(District, id=district_id)
		status_choices = BOOL_CHOICES
		if status:
			forms = MahilaPratinidhiForm.objects.filter(district_id=self.kwargs.get('district_id'), status=status)
		return render(request, self.template_name, {'forms': forms, 'district_id': district_id, 'status_choices': status_choices, 'district': district})


class UserProfileView(LoginRequiredMixin, DetailView):
	model = User
	context_object_name = 'user'
	template_name = 'core/user_profile.html'


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
	model = User
	fields = ('first_name', 'last_name', 'email')
	context_object_name = 'user'
	template_name = 'core/user_profile_update.html'

	def get_success_url(self):
		success_url = reverse_lazy('core:user_profile', args=(self.object.pk,))
		return success_url

