from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView

from .models import MahilaPratinidhiForm, District, BOOL_CHOICES, ProvinceMahilaPratinidhiForm, Province
from .forms import MahilaPratinidhiFormForm, ProvinceMahilaPratinidhiFormForm


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


class ProvinceMahilaPratinidhiFormDetailView(LoginRequiredMixin, DetailView):

	model = ProvinceMahilaPratinidhiForm
	template_name = "core/province_mahila_pratinidhi_detail.html"
	context_object_name = 'form'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['province'] = self.object.province
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


class ProvinceMahilaPratinidhiDashboardView(LoginRequiredMixin, TemplateView):
	template_name = 'core/province_mahila_pratinidhi_dashboard.html'

	def get(self, request, *args, **kwargs):
		forms = ProvinceMahilaPratinidhiForm.objects.filter(province_id=self.kwargs.get('province_id'))
		status = self.request.GET.get('status')
		province_id = self.kwargs.get('province_id')
		# district = District.objects.get(id=district_id)
		province = get_object_or_404(Province, id=province_id)
		status_choices = BOOL_CHOICES
		if status:
			forms = ProvinceMahilaPratinidhiForm.objects.filter(province_id=self.kwargs.get('province_id'), status=status)
		return render(request, self.template_name, {'forms': forms, 'province_id': province_id, 'status_choices': status_choices, 'province': province})



class ProvinceMahilaPratinidhiFormCreateView(LoginRequiredMixin, CreateView):

	model = ProvinceMahilaPratinidhiForm
	form_class = ProvinceMahilaPratinidhiFormForm
	template_name = "core/province_mahila_pratinidhi_form.html"

	def form_valid(self, form):
		form.instance.province = get_object_or_404(Province, pk=self.kwargs['province_id'])
		return super().form_valid(form)

	def get_success_url(self):
		success_url = reverse_lazy('core:province_mahila_pratinidhi_form_dashboard', args=(self.kwargs.get('province_id'),))
		return success_url

	def get_context_data(self, **kwargs):
		context = super(ProvinceMahilaPratinidhiFormCreateView, self).get_context_data(**kwargs)
		context['province'] = Province.objects.get(id=self.kwargs['province_id'])
		return context


class ProvinceUloadView(TemplateView):
	template_name = 'core/province_upload.html'

	def get_context_data(self, **kwargs):
		context = super(ProvinceUloadView, self).get_context_data(**kwargs)
		context['provinces'] = Province.objects.all()
		return context


def province_file_upload(request):
	import pandas as pd

	try:
		request_files = request.FILES.getlist('file')
		print(Province.objects.get(name=request.POST.get('prov')))
		files = [pd.read_excel(filename, sheet_name="province3").fillna(value='') for filename in request_files]

		for df in files:
			total = df['नाम'].count()
			for row in range(0, total):

				ProvinceMahilaPratinidhiForm.objects.get_or_create(
					province=Province.objects.get(name=request.POST.get('prov')),
					name=df['नाम'][row],
					english_name=df['English Name'][row],
					date_of_birth=df['जन्ममिती'][row],
					mothers_name=df['आमाको नाम'][row],
					fathers_name=df['बाबुको नाम'][row],
					marital_status=df['बैवाहिक स्थिति'][row],
					husbands_name=df['श्रीमानको नाम'][row],
					caste=df['जातियता'][row],
					mother_tongue=df['मातृभाषा'][row],
					educational_qualification=df['औपचारिक शैक्षिक योग्यता'][row],
					subject=df['बिषय'][row],
					permanent_address=df['ठेगाना (स्थायी) :  जिल्ला'][row],
					permanent_gapa_napa=df['गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका'][row],
					permanent_ward_no=df['वडा नं'][row],
					permanent_tole=df['टोल'][row],
					temporary_address=df['ठेगाना (अस्थायी) जिल्ला'][row],
					temporary_gapa_napa=df['गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका '][row],
					temporary_ward_no=df['वडा नं'][row],
					temporary_tole=df['टोल'][row],
					mobile=df['मोवाइल'][row],
					contact_number=df['सम्पर्क नं'][row],
					email=df['इमेल'][row],
					social_networking_medium=df['सामाजिक सन्जालका माध्यम (छ भने):'][row],
					nirwachit_prakriya=df['निर्वाचित प्रक्रिया'][row],
					nirwachit_padh=df['निर्वाचित पद'][row],
					pichidiyeko_chhetra_ho_hoina=df['पिछडिएको क्षेत्र हो कि होइन'][row],
					nirwachit_chhetrako_bibaran=df['निर्वाचित क्षेत्रको विवरण'][row],
					nirwachit_vayeko_chhetra_aafno_thegana=df['निर्वाचित भएको क्षेत्र आफ्नो अस्थायी/ स्थायी ठेगाना भन्दा फरक'][row],
					party_name=df['पार्टीको विवरण: पार्टीको नाम'][row],
					party_joined_date=df['पाटींमा संलग्न भएको मिति'][row],
					pramukh_jimmewari=df['प्रमुख जिम्मेवारी'][row],
					nirwachit_chetra_pratiko_pratibadhata=df['निर्वाचित क्षेत्र प्रतिको प्रतिबद्धता'][row],
					aaja_vanda_agadi_chunab_ladnu_vayeko_chha=df['आज भन्दा अघि चुनाब लड्नुभएको छ?'][row],
					prapta_maat_sankhya=df['प्राप्त मत संख्या'][row],
					samlagna_sang_sastha_samuha=df['सलग्न संघ, सस्था , समूह'][row],
				)
		messages.success(request, 'Successfully loaded data from files')
		return HttpResponseRedirect('/province-upload')
	except:
		messages.error(request, "File Format not supported")
		return HttpResponseRedirect('/province-upload')


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