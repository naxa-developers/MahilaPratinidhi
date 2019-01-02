from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView

from .models import MahilaPratinidhiForm, District, BOOL_CHOICES, ProvinceMahilaPratinidhiForm, Province, RastriyaShava, PratinidhiShava
from .forms import MahilaPratinidhiFormForm, ProvinceMahilaPratinidhiFormForm, RastriyaShavaFormForm, PratinidhiShavaFormForm


class MainDashboard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

	template_name = "core/main_dashboard.html"
	

	def test_func(self):
		return self.request.user.is_superuser


class RastriyaShavaDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

	template_name = 'core/rastriya_shava_mahila_pratinidhi_form_dashboard.html'

	def test_func(self):
		return self.request.user.is_superuser

	def get(self, request, *args, **kwargs):
		rastriya_shava_data = RastriyaShava.objects.all()
		return render(request, self.template_name, {'rastriya_shava_datas':rastriya_shava_data})


class RastriyaShavaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

	model = RastriyaShava
	form_class = RastriyaShavaFormForm
	template_name = "core/rastriya_shava_mahila_pratinidhi_form.html"
	
	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:rastriya_shava_form_dashboard')
		return success_url

	def get_context_data(self, **kwargs):
		context = super(RastriyaShavaCreateView, self).get_context_data(**kwargs)
		context['rastriya_shava'] = RastriyaShava.objects.all
		return context

class RastriyaShavaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

	model = RastriyaShava
	template_name = "core/rastriya_shava_mahila_pratinidhi_detail.html"
	context_object_name = 'form'

	def test_func(self):
		return self.request.user.is_superuser


class RastriyaShavaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

	model = RastriyaShava
	form_class = RastriyaShavaFormForm
	template_name = "core/rastriya_shava_mahila_pratinidhi_form.html"

	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:rastriya_shava_form_dashboard')
		return success_url


class RastriyaShavaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

	model = RastriyaShava
	template_name = "core/rastriya_shava_mahila_pratinidhi_delete.html"
	context_object_name = 'form'

	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:rastriya_shava_form_dashboard')
		return success_url

class RastriyaShavaUloadView(UserPassesTestMixin, TemplateView):

	template_name = 'core/rastriya_shava_upload.html'

	def test_func(self):
		return self.request.user.is_superuser


# def rastriya_shava_file_upload(request):
# 	import pandas as pd
# 	try:
# 		request_files = request.FILES.getlist('file')
# 		files = [pd.read_excel(filename).fillna(value='') for filename in request_files]
# 		print(files)
# 		for df in files:
# 			total = df['नाम'].count()
# 			for row in range(0, total):
# 				# import ipdb; ipdb.set_trace()

# 				obj, created =RastriyaShava.objects.get_or_create(
# 					#province=Province.objects.get(name=Province.objects.get(name=df['Province'][0])),
# 					name=df['नाम'][row],
# 					english_name=df['English Name'][row],
# 					date_of_birth=df['जन्ममिती'][row])
					
# 				obj.age=df['उमेर'][row]
# 				obj.mothers_name=df['आमाको नाम'][row]
# 				obj.fathers_name=df['बाबुको नाम'][row]
# 				obj.marital_status=df['बैवाहिक स्थिति'][row]
# 				obj.husbands_name=df['श्रीमानको नाम'][row]
# 				obj.caste=df['जातियता'][row]
# 				obj.mother_tongue=df['मातृभाषा'][row]
# 				obj.educational_qualification=df['औपचारिक शैक्षिक योग्यता'][row]
# 				obj.subject=df['बिषय'][row]
# 				obj.permanent_address=df['ठेगाना (स्थायी) :  जिल्ला'][row]
# 				obj.permanent_gapa_napa=df['गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका'][row]
# 				obj.permanent_ward_no=df['वडा नं'][row]
# 				obj.permanent_tole=df['टोल'][row]
# 				obj.temporary_address=df['ठेगाना (अस्थायी) जिल्ला'][row]
# 				obj.temporary_gapa_napa=df['गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका '][row]
# 				obj.temporary_ward_no=df['वडा नं'][row]
# 				obj.temporary_tole=df['टोल'][row]
# 				obj.mobile=df['मोवाइल'][row]
# 				obj.contact_number=df['सम्पर्क नं'][row]
# 				obj.email=df['इमेल'][row]
# 				obj.social_networking_medium=df['सामाजिक सन्जालका माध्यम (छ भने):'][row]
# 				obj.nirwachit_prakriya=df['निर्वाचित प्रक्रिया'][row]
# 				obj.nirwachit_padh=df['निर्वाचित पद'][row]
# 				obj.pichidiyeko_chhetra_ho_hoina=df['पिछडिएको क्षेत्र हो कि होइन'][row]
# 				obj.nirwachit_chhetrako_bibaran=df['निर्वाचित क्षेत्रको विवरण'][row]
# 				obj.nirwachit_vayeko_chhetra_aafno_thegana=df['निर्वाचित भएको क्षेत्र आफ्नो अस्थायी/ स्थायी ठेगाना भन्दा फरक'][row]
# 				obj.party_name=df['पार्टीको विवरण: पार्टीको नाम'][row]
# 				obj.party_joined_date=df['पाटींमा संलग्न भएको मिति'][row]
# 				obj.pramukh_jimmewari=df['प्रमुख जिम्मेवारी'][row]
# 				obj.nirwachit_chetra_pratiko_pratibadhata=df['निर्वाचित क्षेत्र प्रतिको प्रतिबद्धता'][row]
# 				obj.aaja_vanda_agadi_chunab_ladnu_vayeko_chha=df['आज भन्दा अघि चुनाब लड्नुभएको छ?'][row]
# 				obj.prapta_maat_sankhya=df['प्राप्त मत संख्या'][row]
# 				obj.samlagna_sang_sastha_samuha=df['सलग्न संघ, सस्था , समूह'][row]
# 				obj.samitima_vumika=df['समितिमा पद'][row]
# 				obj.samlagna_samsadiya_samiti=df['संलग्न समिति'][row]
# 				obj.save()
# 		messages.success(request, 'Successfully loaded data from files')
# 		return HttpResponseRedirect('/cms/rastriya-shava-upload')
# 	except Exception as e:
# 		print(e)
# 		messages.error(request, "File Format not supported")
# 		return HttpResponseRedirect('/cms/rastriya-shava-upload')


def rastriya_shava_file_upload(request):
	import pandas as pd
	try:
		request_files = request.FILES.getlist('file')
		files = [pd.read_excel(filename).fillna(value='') for filename in request_files]
		print(files)
		for df in files:
			total = df['Name_EN'].count()
			for row in range(1, total+1):
				# import ipdb; ipdb.set_trace()

				obj, created =RastriyaShava.objects.get_or_create(
					province=Province.objects.get(name=df['Province'][row]),
					name=df['Name_NE'][row],
					english_name=df['Name_EN'][row],
					date_of_birth=df['Date of Birth_NE'][row])
				
				if df['Age_EN'][row]:
					obj.age=df['Age_EN'][row]
				else:
					obj.age=None	
				if df['Age_NE'][row]:
					obj.age_ne_NP=df['Age_NE'][row]
				else:
					obj.age_ne_NP=None			
				# obj.age_ne_NP=int(df['Age_NE'][row])
				obj.mothers_name=df["Mother's.Name_EN"][row]
				obj.mothers_name_ne_NP=df["Mother's.Name_NE"][row]
				obj.fathers_name=df["Father's.Name_EN"][row]
				obj.fathers_name_ne_NP=df["Father's.Name_NE"][row]
				obj.marital_status=df['Maritial.Status_EN'][row]
				obj.marital_status_ne_NP=df['Maritial.Status_NE'][row]
				obj.husbands_name=df["Spouse's.Name_EN"][row]
				obj.husbands_name_ne_NP=df["Spouse's.Name_NE"][row]
				obj.caste=df['Ethnicity_EN'][row]
				obj.caste_ne_NP=df['Ethnicity_NE'][row]
				obj.mother_tongue=df['Mother.Tongue_EN'][row]
				obj.mother_tongue_ne_NP=df['Mother.Tongue_NE'][row]
				obj.educational_qualification=df['Formal.Education_EN'][row]
				obj.educational_qualification_ne_NP=df['Formal.Education_NE'][row]
				obj.subject=df['Degree.Name_EN'][row]
				obj.subject_ne_NP=df['Degree.Name_NE'][row]
				obj.permanent_address=df['Address (Permanent: District)_EN'][row]
				obj.permanent_address_ne_NP=df['Address (Permanent: District)_NE'][row]
				obj.permanent_gapa_napa=df['Village / Municipality / Sub-Metropolitan Municipality_EN'][row]
				obj.permanent_gapa_napa_ne_NP=df['Village / Municipality / Sub-Metropolitan Municipality_NE'][row]
				obj.permanent_ward_no=df['Ward_EN'][row]
				obj.permanent_ward_no_ne_NP=df['Ward_NE'][row]
				obj.permanent_tole=df['Street_EN'][row]
				obj.permanent_tole_ne_NP=df['Street_NE'][row]
				obj.temporary_address=df['Address (Temporary: District)_EN'][row]
				obj.temporary_address_ne_NP=df['Address (Temporary: District)_NE'][row]
				obj.temporary_gapa_napa=df['Temporary_Village / Municipality / Sub-Metropolitan Municipality_EN'][row]
				obj.temporary_gapa_napa_ne_NP=df['Temporary_Village / Municipality / Sub-Metropolitan Municipality_NE'][row]
				obj.temporary_ward_no=df['Temporary_Ward_EN'][row]
				obj.temporary_ward_no_ne_NP=df['Temporary_Ward_NE'][row]
				obj.temporary_tole=df['Temporary_Street_EN'][row]
				obj.temporary_tole_ne_NP=df['Temporary_Street_NE'][row]
				obj.mobile=df['Mobile_EN'][row]
				obj.mobile_ne_NP=df['Mobile_NE'][row]
				obj.contact_number=df['Contact.No_EN'][row]
				obj.contact_number_ne_NP=df['Contact.No_EN'][row]
				obj.email=df['Email'][row]
				obj.social_networking_medium=df['Social Media_EN'][row]
				obj.social_networking_medium_ne_NP=df['Social Media_EN'][row]
				obj.nirwachit_prakriya=df['Election.Type_EN'][row]
				obj.nirwachit_prakriya_ne_NP=df['Election.Type_NE'][row]
				obj.nirwachit_padh=df['Elected.Post_EN'][row]
				obj.nirwachit_padh_ne_NP=df['Elected.Post_NE'][row]
				obj.pichidiyeko_chhetra_ho_hoina=df['Is your area listed in Government of Nepal’s backward area?_EN'][row]
				obj.pichidiyeko_chhetra_ho_hoina_ne_NP=df['Is your area listed in Government of Nepal’s backward area?_NE'][row]
				obj.nirwachit_chhetrako_bibaran=df['Description of Elected Area_EN'][row]
				obj.nirwachit_chhetrako_bibaran_ne_NP=df['Description of Elected Area_NE'][row]
				obj.nirwachit_vayeko_chhetra_aafno_thegana=df['Is the elected constituency different than the address of the representative (Yes/No)?_EN'][row]
				obj.nirwachit_vayeko_chhetra_aafno_thegana_ne_NP=df['Is the elected constituency different than the address of the representative (Yes/No)?_NE'][row]
				obj.party_name=df['Name.of.Party_EN'][row]
				obj.party_name_ne_NP=df['Name.of.Party_NE'][row]
				obj.party_joined_date=df['Date.of.affiliation.with.Party_EN'][row]
				obj.party_joined_date_ne_NP=df['Date.of.affiliation.with.Party_NE'][row]
				obj.pramukh_jimmewari=df['Major.Respnsibility_EN'][row]
				obj.pramukh_jimmewari_ne_NP=df['Major.Respnsibility_NE'][row]
				obj.nirwachit_chetra_pratiko_pratibadhata=df['Political.Commitment_EN'][row]
				obj.nirwachit_chetra_pratiko_pratibadhata_ne_NP=df['Political.Commitment_NE'][row]
				obj.aaja_vanda_agadi_chunab_ladnu_vayeko_chha=df['Have.you.participated.in.an.election.before?_EN'][row]
				obj.aaja_vanda_agadi_chunab_ladnu_vayeko_chha_ne_NP=df['Have.you.participated.in.an.election.before?_NE'][row]
				obj.prapta_maat_sankhya=df['Number.of.votes.received_EN'][row]
				obj.prapta_maat_sankhya_ne_NP=df['Number.of.votes.received_NE'][row]
				obj.samlagna_sang_sastha_samuha=df['Details.of.the.recent.union, organization, group.you.are.engaged.with?_EN'][row]
				obj.samlagna_sang_sastha_samuha_ne_NP=df['Details.of.the.recent.union, organization, group.you.are.engaged.with?_NE'][row]
				obj.samitima_vumika=df['Role.in.organization_EN'][row]
				obj.samitima_vumika_ne_NP=df['Role.in.organization_NE'][row]
				# obj.samlagna_samsadiya_samiti=df['संलग्न समिति'][row]
				obj.save()
		messages.success(request, 'Successfully loaded data from files')
		return HttpResponseRedirect('/cms/rastriya-shava-upload')
	except Exception as e:
		print(e.__class__.__name__ + " " + str(e))
		messages.error(request, "File Format not supported")
		return HttpResponseRedirect('/cms/rastriya-shava-upload')


class PratinidhiShavaDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
	template_name = 'core/pratinidhi_shava_mahila_pratinidhi_form_dashboard.html'

	def test_func(self):
		return self.request.user.is_superuser

	def get(self, request, *args, **kwargs):
		pratinidhi_shava_data = PratinidhiShava.objects.all()
		return render(request, self.template_name, {'pratinidhi_shava_datas':pratinidhi_shava_data})


class PratinidhiShavaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

	model = PratinidhiShava
	form_class = PratinidhiShavaFormForm
	template_name = "core/pratinidhi_shava_mahila_pratinidhi_form.html"

	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:pratinidhi_shava_form_dashboard')
		return success_url

	def get_context_data(self, **kwargs):
		context = super(PratinidhiShavaCreateView, self).get_context_data(**kwargs)
		context['pratinidhi_shava'] = PratinidhiShava.objects.all
		return context

class PratinidhiShavaDetailView(LoginRequiredMixin, DetailView):

	model = PratinidhiShava
	template_name = "core/pratinidhi_shava_mahila_pratinidhi_detail.html"
	context_object_name = 'form'


class PratinidhiShavaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

	model = PratinidhiShava
	form_class = PratinidhiShavaFormForm
	template_name = "core/pratinidhi_shava_mahila_pratinidhi_form.html"

	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:pratinidhi_shava_form_dashboard')
		return success_url


class PratinidhiShavaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

	model = PratinidhiShava
	template_name = "core/pratinidhi_shava_mahila_pratinidhi_delete.html"
	context_object_name = 'form'

	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:pratinidhi_shava_form_dashboard')
		return success_url

class PratinidhiShavaUloadView(UserPassesTestMixin, TemplateView):
	template_name = 'core/pratinidhi_shava_upload.html'

	def test_func(self):
		return self.request.user.is_superuser


# def pratinidhi_shava_file_upload(request):
# 	import pandas as pd
# 	try:
# 		request_files = request.FILES.getlist('file')
# 		files = [pd.read_excel(filename).fillna(value='') for filename in request_files]
# 		print(files)
# 		for df in files:
# 			total = df['नाम'].count()
# 			for row in range(0, total):

# 				obj, created=PratinidhiShava.objects.get_or_create(
# 					#province=Province.objects.get(name=Province.objects.get(name=df['Province'][0])),
# 					name=df['नाम'][row],
# 					english_name=df['English Name'][row],
# 					date_of_birth=df['जन्ममिती'][row])

# 				obj.age=df['उमेर'][row]
# 				obj.mothers_name=df['आमाको नाम'][row]
# 				obj.fathers_name=df['बाबुको नाम'][row]
# 				obj.marital_status=df['बैवाहिक स्थिति'][row]
# 				obj.husbands_name=df['श्रीमानको नाम'][row]
# 				obj.caste=df['जातियता'][row]
# 				obj.mother_tongue=df['मातृभाषा'][row]
# 				obj.educational_qualification=df['औपचारिक शैक्षिक योग्यता'][row]
# 				obj.subject=df['बिषय'][row]
# 				obj.permanent_address=df['ठेगाना (स्थायी) :  जिल्ला'][row]
# 				obj.permanent_gapa_napa=df['गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका'][row]
# 				obj.permanent_ward_no=df['वडा नं'][row]
# 				obj.permanent_tole=df['टोल'][row]
# 				obj.temporary_address=df['ठेगाना (अस्थायी) जिल्ला'][row]
# 				obj.temporary_gapa_napa=df['गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका '][row]
# 				obj.emporary_ward_no=df['वडा नं'][row]
# 				obj.temporary_tole=df['टोल'][row]
# 				obj.mobile=df['मोवाइल'][row]
# 				obj.contact_number=df['सम्पर्क नं'][row]
# 				obj.email=df['इमेल'][row]
# 				obj.social_networking_medium=df['सामाजिक सन्जालका माध्यम (छ भने):'][row]
# 				obj.nirwachit_prakriya=df['निर्वाचित प्रक्रिया'][row]
# 				obj.nirwachit_padh=df['निर्वाचित पद'][row]
# 				obj.pichidiyeko_chhetra_ho_hoina=df['पिछडिएको क्षेत्र हो कि होइन'][row]
# 				obj.nirwachit_chhetrako_bibaran=df['निर्वाचित क्षेत्रको विवरण'][row]
# 				obj.nirwachit_vayeko_chhetra_aafno_thegana=df['निर्वाचित भएको क्षेत्र आफ्नो अस्थायी/ स्थायी ठेगाना भन्दा फरक'][row]
# 				obj.party_name=df['पार्टीको विवरण: पार्टीको नाम'][row]
# 				obj.party_joined_date=df['पाटींमा संलग्न भएको मिति'][row]
# 				obj.pramukh_jimmewari=df['प्रमुख जिम्मेवारी'][row]
# 				obj.nirwachit_chetra_pratiko_pratibadhata=df['निर्वाचित क्षेत्र प्रतिको प्रतिबद्धता'][row]
# 				obj.aaja_vanda_agadi_chunab_ladnu_vayeko_chha=df['आज भन्दा अघि चुनाब लड्नुभएको छ?'][row]
# 				obj.prapta_maat_sankhya=df['प्राप्त मत संख्या'][row]
# 				obj.samlagna_sang_sastha_samuha=df['सलग्न संघ, सस्था , समूह'][row]
# 				obj.samitima_vumika=df['समितिमा भूमिका'][row]
# 				obj.samlagna_samsadiya_samiti=df['संलग्न संसदीय समिति'][row]
# 				obj.save()
# 		messages.success(request, 'Successfully loaded data from files')
# 		return HttpResponseRedirect('/cms/pratinidhi-shava-upload')
# 	except Exception as e:
# 		print(e)
# 		messages.error(request, "File Format not supported")
# 		return HttpResponseRedirect('/cms/pratinidhi-shava-upload')


def pratinidhi_shava_file_upload(request):
	import pandas as pd
	try:
		request_files = request.FILES.getlist('file')
		files = [pd.read_excel(filename).fillna(value='') for filename in request_files]
		print(files)
		for df in files:
			total = df['Name_EN'].count()
			for row in range(1, total+1):
				# import ipdb; ipdb.set_trace()

				obj, created =PratinidhiShava.objects.get_or_create(
					province=Province.objects.get(name=df['Province'][row]),
					name=df['Name_NE'][row],
					english_name=df['Name_EN'][row],
					date_of_birth=str(df['Date of Birth_NE'][row])[:10])
				
				if df['Age_EN'][row]:
					obj.age=df['Age_EN'][row]
				else:
					obj.age=None	
				if df['Age_NE'][row]:
					obj.age_ne_NP=df['Age_NE'][row]
				else:
					obj.age_ne_NP=None			
				# obj.age_ne_NP=int(df['Age_NE'][row])
				obj.mothers_name=df["Mother's.Name_EN"][row]
				obj.mothers_name_ne_NP=df["Mother's.Name_NE"][row]
				obj.fathers_name=df["Father's.Name_EN"][row]
				obj.fathers_name_ne_NP=df["Father's.Name_NE"][row]
				obj.marital_status=df['Maritial.Status_EN'][row]
				obj.marital_status_ne_NP=df['Maritial.Status_NE'][row]
				obj.husbands_name=df["Spouse's.Name_EN"][row]
				obj.husbands_name_ne_NP=df["Spouse's.Name_NE"][row]
				obj.caste=df['Ethnicity_EN'][row]
				obj.caste_ne_NP=df['Ethnicity_NE'][row]
				obj.mother_tongue=df['Mother.Tongue_EN'][row]
				obj.mother_tongue_ne_NP=df['Mother.Tongue_NE'][row]
				obj.educational_qualification=df['Formal.Education_EN'][row]
				obj.educational_qualification_ne_NP=df['Formal.Education_NE'][row]
				obj.subject=df['Degree.Name_EN'][row]
				obj.subject_ne_NP=df['Degree.Name_NE'][row]
				obj.permanent_address=df['Address (Permanent: District)_EN'][row]
				obj.permanent_address_ne_NP=df['Address (Permanent: District)_NE'][row]
				obj.permanent_gapa_napa=df['Village / Municipality / Sub-Metropolitan Municipality_EN'][row]
				obj.permanent_gapa_napa_ne_NP=df['Village / Municipality / Sub-Metropolitan Municipality_NE'][row]
				obj.permanent_ward_no=df['Ward_EN'][row]
				obj.permanent_ward_no_ne_NP=df['Ward_NE'][row]
				obj.permanent_tole=df['Street_EN'][row]
				obj.permanent_tole_ne_NP=df['Street_NE'][row]
				obj.temporary_address=df['Address (Temporary: District)_EN'][row]
				obj.temporary_address_ne_NP=df['Address (Temporary: District)_NE'][row]
				obj.temporary_gapa_napa=df['Temporary_Village / Municipality / Sub-Metropolitan Municipality_EN'][row]
				obj.temporary_gapa_napa_ne_NP=df['Temporary_Village / Municipality / Sub-Metropolitan Municipality_NE'][row]
				obj.temporary_ward_no=df['Temporary_Ward_EN'][row]
				obj.temporary_ward_no_ne_NP=df['Temporary_Ward_NE'][row]
				obj.temporary_tole=df['Temporary_Street_EN'][row]
				obj.temporary_tole_ne_NP=df['Temporary_Street_NE'][row]
				obj.mobile=df['Mobile_EN'][row]
				obj.mobile_ne_NP=df['Mobile_NE'][row]
				obj.contact_number=df['Contact.No_EN'][row]
				obj.contact_number_ne_NP=df['Contact.No_EN'][row]
				obj.email=df['Email'][row]
				obj.social_networking_medium=df['Social Media_EN'][row]
				obj.social_networking_medium_ne_NP=df['Social Media_EN'][row]
				obj.nirwachit_prakriya=df['Election.Type_EN'][row]
				obj.nirwachit_prakriya_ne_NP=df['Election.Type_NE'][row]
				obj.nirwachit_padh=df['Elected.Post_EN'][row]
				obj.nirwachit_padh_ne_NP=df['Elected.Post_NE'][row]
				obj.pichidiyeko_chhetra_ho_hoina=df['Is your area listed in Government of Nepal’s backward area?_EN'][row]
				obj.pichidiyeko_chhetra_ho_hoina_ne_NP=df['Is your area listed in Government of Nepal’s backward area?_NE'][row]
				obj.nirwachit_chhetrako_bibaran=df['Description of Elected Area_EN'][row]
				obj.nirwachit_chhetrako_bibaran_ne_NP=df['Description of Elected Area_NE'][row]
				obj.nirwachit_vayeko_chhetra_aafno_thegana=df['Is the elected constituency different than the address of the representative (Yes/No)?_EN'][row]
				obj.nirwachit_vayeko_chhetra_aafno_thegana_ne_NP=df['Is the elected constituency different than the address of the representative (Yes/No)?_NE'][row]
				obj.party_name=df['Name.of.Party_EN'][row]
				obj.party_name_ne_NP=df['Name.of.Party_NE'][row]
				obj.party_joined_date=df['Date.of.affiliation.with.Party_EN'][row]
				obj.party_joined_date_ne_NP=df['Date.of.affiliation.with.Party_NE'][row]
				obj.pramukh_jimmewari=df['Major.Respnsibility_EN'][row]
				obj.pramukh_jimmewari_ne_NP=df['Major.Respnsibility_NE'][row]
				obj.nirwachit_chetra_pratiko_pratibadhata=df['Political.Commitment_EN'][row]
				obj.nirwachit_chetra_pratiko_pratibadhata_ne_NP=df['Political.Commitment_NE'][row]
				obj.aaja_vanda_agadi_chunab_ladnu_vayeko_chha=df['Have.you.participated.in.an.election.before?_EN'][row]
				obj.aaja_vanda_agadi_chunab_ladnu_vayeko_chha_ne_NP=df['Have.you.participated.in.an.election.before?_NE'][row]
				obj.prapta_maat_sankhya=df['Number.of.votes.received_EN'][row]
				obj.prapta_maat_sankhya_ne_NP=df['Number.of.votes.received_NE'][row]
				obj.samlagna_sang_sastha_samuha=df['Details.of.the.recent.union, organization, group.you.are.engaged.with?_EN'][row]
				obj.samlagna_sang_sastha_samuha_ne_NP=df['Details.of.the.recent.union, organization, group.you.are.engaged.with?_NE'][row]
				obj.samitima_vumika=df['Role.in.organization_EN'][row]
				obj.samitima_vumika_ne_NP=df['Role.in.organization_NE'][row]
				obj.save()
		messages.success(request, 'Successfully loaded data from files')
		return HttpResponseRedirect('/cms/pratinidhi-shava-file-upload')
	except Exception as e:
		print(e.__class__.__name__ + " " + str(e))
		messages.error(request, "File Format not supported")
		return HttpResponseRedirect('/cms/pratinidhi-shava-file-upload')



class Dashboard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

	template_name = "core/dashboard.html"
	
	def test_func(self):
		return self.request.user.is_superuser

	def get(self, request, *args, **kwargs):
		districts = District.objects.all()
		district = request.GET.get('dist')
		district = District.objects.filter(name=district)

		return render(request, self.template_name, {'districts': districts, 'district': district})

class MahilaPratinidhiDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
	template_name = 'core/mahila_pratinidhi_dashboard.html'

	def test_func(self):
		return self.request.user.is_superuser

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

class MahilaPratinidhiFormCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

	model = MahilaPratinidhiForm
	form_class = MahilaPratinidhiFormForm
	template_name = "core/mahila_pratinidhi_form.html"

	def test_func(self):
		return self.request.user.is_superuser

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


class MahilaPratinidhiFormDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

	model = MahilaPratinidhiForm
	template_name = "core/mahila_pratinidhi_detail.html"
	context_object_name = 'form'

	def test_func(self):
		return self.request.user.is_superuser

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['district'] = self.object.district
		return context

class MahilaPratinidhiFormUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

	model = MahilaPratinidhiForm
	form_class = MahilaPratinidhiFormForm
	success_url = reverse_lazy('core:dashboard')
	template_name = "core/mahila_pratinidhi_form.html"

	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:mahila_pratinidhi_form_dashboard', args=(self.object.district.pk,))
		return success_url

	def get_context_data(self, **kwargs):
		context = super(MahilaPratinidhiFormUpdateView, self).get_context_data(**kwargs)
		context['district'] = MahilaPratinidhiForm.objects.get(id=self.kwargs['pk']).district
		context['is_update_form'] = True
		return context


class MahilaPratinidhiFormDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

	model = MahilaPratinidhiForm
	template_name = "core/mahila_pratinidhi_delete.html"
	context_object_name = 'form'

	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:mahila_pratinidhi_form_dashboard', args=(self.object.district.pk,))
		return success_url

	def get_context_data(self, **kwargs):
		context = super(MahilaPratinidhiFormDeleteView, self).get_context_data(**kwargs)
		context['district'] = self.object.district
		return context


class UloadView(UserPassesTestMixin, TemplateView):
	template_name = 'core/upload.html'

	def test_func(self):
		return self.request.user.is_superuser

	def get_context_data(self, **kwargs):
		context = super(UloadView, self).get_context_data(**kwargs)
		context['districts'] = District.objects.all()
		return context


# def file_upload(request):
# 	import pandas as pd

# 	try:

# 		request_files = request.FILES.getlist('file')
# 		files = [pd.read_excel(filename).fillna(value='') for filename in request_files]
# 		for df in files:
# 			total = df['qm=;+'].count()

# 			for row in range(0, total):
# 				print(request.POST.get('dist'))

# 				obj, created = MahilaPratinidhiForm.objects.create(
# 					district=District.objects.get(name=request.POST.get('dist')),
# 					name=df['gfd'][row],
# 					age=df['pd]/'][row])

# 				obj.marital_status=df['j}jflxs l:lYft'][row]
# 				obj.educational_qualification=df['z}lIfs of]Uotf'][row]
# 				obj.caste=df['hfltotf'][row]
# 				obj.address=df['7]ufgf'][row]
# 				obj.contact_number=df[';Dks{ g '][row]
# 				obj.email=df['Od]n 7]ufgf'][row]
# 				obj.nirwachit_padh=df['lgjf{lrt kb'][row]
# 				obj.nirwachit_vdc_or_municipality_name=df['lgjf{lrt uf lj ; tyf gu/kflnsfsf]] gfd '][row]
# 				obj.party_name=df['kf6L{sf] gfd '][row]
# 				obj.party_joined_date=df['kf6L{df ;++++nUg ePsf] ldtL'][row]
# 				obj.samlagna_sang_sastha_samuha=df[' ;++++nUg ;++3 ;F:yf ;d"x  '][row]
# 				obj.nirwachit_chetra_pratiko_pratibadhata=df['lgjf{lrt Ifq k||ltsf] k|ltaM4tf '][row]
# 				obj.save()
# 		messages.success(request, 'Successfully loaded data from files')
# 		return HttpResponseRedirect('/cms/upload')
# 	except KeyError as e:
# 		print(e)
# 		messages.error(request, "File Format not supported")
# 		return HttpResponseRedirect('/cms/upload')


#for english and nepali file upload
# def file_upload(request):
# 	import pandas as pd
#
# 	try:
#
# 		request_files = request.FILES.getlist('file')
# 		files = [pd.read_excel(filename).fillna(value='') for filename in request_files]
# 		for df in files:
# 			total = df['S.N'].count()
#
# 			for row in range(0, total):
#
# 				obj = MahilaPratinidhiForm.objects.create(
# 					district=District.objects.get(name=request.POST.get('dist')),
# 					name=df['Name_EN'][row],
# 					age=df['Age_EN'][row])
# 				obj.label = df['Label_EN'][row]
# 				obj.label_ne_NP = df['Label_NE'][row]
#
# 				obj.name_ne_NP=df['Name_NE'][row]
# 				obj.age_ne_NP=int(df['Age_NE'][row])
# 				obj.marital_status=df['Maritial_Status_EN'][row]
# 				obj.marital_status_ne_NP=df['Maritial_Status_NE'][row]
# 				obj.educational_qualification=df['Educational_Status_EN'][row]
# 				obj.educational_qualification_ne_NP=df['Educational_Status_NE'][row]
# 				obj.caste=df['Ethnicity_EN'][row]
# 				obj.caste_ne_NP=df['Ethnicity_NE'][row]
# 				obj.address=df['Location_EN'][row]
# 				obj.address_ne_NP=df['Location_NE'][row]
# 				obj.contact_number=df['Contact_Number_EN'][row]
# 				obj.contact_number_ne_NP=df['Contact_Number_NE'][row]
# 				obj.email=df['Email_Address'][row]
# 				obj.nirwachit_padh=df['Elected_Post_EN'][row]
# 				obj.nirwachit_padh_ne_NP=df['Elected_Post_NE'][row]
# 				obj.nirwachit_vdc_or_municipality_name=df['Name_of _Elected_region_EN'][row]
# 				obj.nirwachit_vdc_or_municipality_name_ne_NP=df['Name_of _Elected_region_NE'][row]
# 				obj.party_name=df['Name_of_Party_EN'][row]
# 				obj.party_name_ne_NP=df['Name_of_Party_NE'][row]
# 				obj.party_joined_date=df['Date_of_Affiliation_with_Party_EN'][row]
# 				obj.party_joined_date_ne_NP=df['Date_of_Affiliation_with_Party_NE'][row]
# 				obj.samlagna_sang_sastha_samuha=df['Affiliated_Institutions_En'][row]
# 				obj.samlagna_sang_sastha_samuha_ne_NP=df['Affiliated_Institutions_NE'][row]
# 				obj.nirwachit_chetra_pratiko_pratibadhata=df['Responsibilities_towards_elected_region_EN'][row]
# 				obj.nirwachit_chetra_pratiko_pratibadhata_ne_NP=df['Responsibilities_towards_elected_region_NE'][row]
# 				obj.province_id=int(df['PROVINCE'][row])
#
#
# 				obj.save()
# 		messages.success(request, 'Successfully loaded data from files')
# 		return HttpResponseRedirect('/cms/upload')
# 	except KeyError as e:
# 		print(e)
# 		messages.error(request, "File Format not supported")
# 		return HttpResponseRedirect('/cms/upload')

#updated nepali and english file_upload for local
def file_upload(request):
	import pandas as pd

	try:

		request_files = request.FILES.getlist('file')
		files = [pd.read_excel(filename).fillna(value='') for filename in request_files]
		for df in files:
			total = df['S.N'].count()

			for row in range(0, total):
				# import ipdb
				# ipdb.set_trace()
				MahilaPratinidhiForm.objects.get_or_create(
					district=District.objects.get(name=df['District'][0]),
					name=df['Name_EN'][row],
					# age=df['Age_EN'][row],)
				name_ne_NP = df['Name_NE'][row],
				# age_ne_NP = int(df['Age_NE'][row],)
				name_of_elected_region_ne_NP = df['Name.of.elected.region_NE'][row],
				name_of_elected_region = df['Name.of.elected.region_EN'][row],
				hlcit_code = df['HLCIT_CODE'][row],
				nirwachit_padh_ne_NP = df['Elected.Post_NE'][row],
				nirwachit_padh = df['Elected.Post_EN'][row],
				ward = df['Ward_EN'][row],
				marital_status_ne_NP = df['Maritial.Status_NE'][row],
				marital_status = df['Maritial.Status_EN'][row],
				educational_qualification_ne_NP = df['Education.Status_NE'][row],
				educational_qualification = df['Education.Status_EN'][row],
				caste_ne_NP = df['Ethnicity_NE'][row],
				caste = df['Ethnicity_EN'][row],
				contact_number = df['Contact.Number_EN'][row],
				# contact_number_ne_NP = df['Contact_Number_NE'][row],
				email = df['Email_EN'][row],
				party_joined_date = df['Date.of.Affiliation.with.Party_EN'][row],
				# party_joined_date_ne_NP = df['Date_of_Affiliation_with_Party_NE'][row],
				samlagna_sang_sastha_samuha_ne_NP = df['Affiliated.Institutions_NE'][row],
				samlagna_sang_sastha_samuha = df['Affiliated.Institutions_EN'][row],
				nirwachit_chetra_pratiko_pratibadhata_ne_NP = df['Political.Commitment_NE'][row],
				nirwachit_chetra_pratiko_pratibadhata = df['Political.Commitment_EN'][row],
				party_name_ne_NP = df['Political.Party_NE'][row],
				party_name = df['Political.Party_EN'][row],
				prapta_maat_sankhya = df['Number.of.Votes.Received_EN'][row],
				# prapta_maat_sankhya_ne_NP = df['Prapta_Mat_NE'][row],
				fathers_name_ne_NP = df["Father's.Name_NE"][row],
				fathers_name = df["Father's.Name_EN"][row],
				mothers_name_ne_NP = df["Mother's.Name_NE"][row],
				mothers_name = df["Mother's.Name_EN"][row],
				dob = df['Date.of.birth_EN'][row])
				# dob_ne_NP = df['DOB_NE'][row],

		messages.success(request, 'Successfully loaded data from files')
		return HttpResponseRedirect('/cms/upload')
	except KeyError as e:
		print(e)
		messages.error(request, "File Format not supported")
		return HttpResponseRedirect('/cms/upload')


class ProvinceDashboard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

	template_name = "core/province_dashboard.html"

	def test_func(self):
		return self.request.user.is_superuser

	def get(self, request, *args, **kwargs):
		provinces = Province.objects.all()
		province = request.GET.get('prov')
		province = Province.objects.filter(name=province)

		return render(request, self.template_name, {'provinces': provinces, 'province': province})

class ProvinceMahilaPratinidhiDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
	template_name = 'core/province_mahila_pratinidhi_dashboard.html'

	def test_func(self):
		return self.request.user.is_superuser

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



class ProvinceMahilaPratinidhiFormCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

	model = ProvinceMahilaPratinidhiForm
	form_class = ProvinceMahilaPratinidhiFormForm
	template_name = "core/province_mahila_pratinidhi_form.html"

	def test_func(self):
		return self.request.user.is_superuser

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

class ProvinceMahilaPratinidhiFormDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

	model = ProvinceMahilaPratinidhiForm
	template_name = "core/province_mahila_pratinidhi_detail.html"
	context_object_name = 'form'

	def test_func(self):
		return self.request.user.is_superuser

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['province'] = self.object.province
		return context


class ProvinceMahilaPratinidhiFormUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

	model = ProvinceMahilaPratinidhiForm
	form_class = ProvinceMahilaPratinidhiFormForm
	template_name = "core/province_mahila_pratinidhi_form.html"

	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:province_mahila_pratinidhi_form_dashboard', args=(self.object.province.pk,))
		return success_url

	def get_context_data(self, **kwargs):
		context = super(ProvinceMahilaPratinidhiFormUpdateView, self).get_context_data(**kwargs)
		context['province'] = ProvinceMahilaPratinidhiForm.objects.get(id=self.kwargs['pk']).province
		context['is_update_form'] = True
		return context


class ProvinceMahilaPratinidhiFormDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

	model = ProvinceMahilaPratinidhiForm
	template_name = "core/province_mahila_pratinidhi_delete.html"
	context_object_name = 'form'

	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:province_mahila_pratinidhi_form_dashboard', args=(self.object.province.pk,))
		return success_url

	def get_context_data(self, **kwargs):
		context = super(ProvinceMahilaPratinidhiFormDeleteView, self).get_context_data(**kwargs)
		context['province'] = self.object.province
		return context


class ProvinceUloadView(UserPassesTestMixin, TemplateView):
	template_name = 'core/province_upload.html'

	def test_func(self):
		return self.request.user.is_superuser

	def get_context_data(self, **kwargs):
		context = super(ProvinceUloadView, self).get_context_data(**kwargs)
		context['provinces'] = Province.objects.all()
		return context


# def province_file_upload(request):
# 	import pandas as pd

# 	try:
# 		request_files = request.FILES.getlist('file')
# 		files = [pd.read_excel(filename).fillna(value='') for filename in request_files]

# 		for df in files:
# 			total = df['नाम'].count()

# 			for row in range(0, total):

# 				obj, created = ProvinceMahilaPratinidhiForm.objects.get_or_create(
# 					province=Province.objects.get(name=Province.objects.get(name=df['Province'][0])),
# 					name=df['नाम'][row],,
# 					english_name=df['English Name'][row],
# 					date_of_birth=df['जन्ममिती'][row])

# 				obj.age=df['उमेर'][row]
# 				obj.mothers_name=df['आमाको नाम'][row]
# 				obj.fathers_name=df['बाबुको नाम'][row]
# 				obj.marital_status=df['बैवाहिक स्थिति'][row]
# 				obj.husbands_name=df['श्रीमानको नाम'][row]
# 				obj.caste=df['जातियता'][row]
# 				obj.mother_tongue=df['मातृभाषा'][row]
# 				obj.educational_qualification=df['औपचारिक शैक्षिक योग्यता'][row]
# 				obj.subject=df['बिषय'][row]
# 				obj.permanent_address=df['ठेगाना (स्थायी) :  जिल्ला'][row]
# 				obj.permanent_gapa_napa=df['गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका'][row]
# 				obj.permanent_ward_no=df['वडा नं'][row]
# 				obj.permanent_tole=df['टोल'][row]
# 				obj.temporary_address=df['ठेगाना (अस्थायी) जिल्ला'][row]
# 				obj.temporary_gapa_napa=df['गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका '][row]
# 				obj.temporary_ward_no=df['वडा नं'][row]
# 				obj.temporary_tole=df['टोल'][row]
# 				obj.mobile=df['मोवाइल'][row]
# 				obj.contact_number=df['सम्पर्क नं'][row]
# 				obj.email=df['इमेल'][row]
# 				obj.social_networking_medium=df['सामाजिक सन्जालका माध्यम (छ भने):'][row]
# 				obj.nirwachit_prakriya=df['निर्वाचित प्रक्रिया'][row]
# 				obj.nirwachit_padh=df['निर्वाचित पद'][row]
# 				obj.pichidiyeko_chhetra_ho_hoina=df['पिछडिएको क्षेत्र हो कि होइन'][row]
# 				obj.nirwachit_chhetrako_bibaran=df['निर्वाचित क्षेत्रको विवरण'][row]
# 				obj.nirwachit_vayeko_chhetra_aafno_thegana=df['निर्वाचित भएको क्षेत्र आफ्नो अस्थायी/ स्थायी ठेगाना भन्दा फरक'][row]
# 				obj.party_name=df['पार्टीको विवरण: पार्टीको नाम'][row]
# 				obj.party_joined_date=df['पाटींमा संलग्न भएको मिति'][row]
# 				obj.pramukh_jimmewari=df['प्रमुख जिम्मेवारी'][row]
# 				obj.nirwachit_chetra_pratiko_pratibadhata=df['निर्वाचित क्षेत्र प्रतिको प्रतिबद्धता'][row]
# 				obj.aaja_vanda_agadi_chunab_ladnu_vayeko_chha=df['आज भन्दा अघि चुनाब लड्नुभएको छ?'][row]
# 				obj.prapta_maat_sankhya=df['प्राप्त मत संख्या'][row]
# 				obj.samlagna_sang_sastha_samuha=df['सलग्न संघ, सस्था , समूह'][row]
# 				obj.save()
# 		messages.success(request, 'Successfully loaded data from files')
# 		return HttpResponseRedirect('/cms/province-upload')
# 	except KeyError as e:
# 		print(e)
# 		messages.error(request, "File Format not supported")
# 		return HttpResponseRedirect('/cms/province-upload')


def province_file_upload(request):
	import pandas as pd
	try:
		request_files = request.FILES.getlist('file')
		files = [pd.read_excel(filename).fillna(value='') for filename in request_files]
		for df in files:
			total = df['Name_EN'].count()
			for row in range(1, total+1):
				obj, created=ProvinceMahilaPratinidhiForm.objects.get_or_create(
					province=Province.objects.get(name=df['Province'][1]),
					name=df['Name_NE'][row],
					english_name=df['Name_EN'][row],
					date_of_birth=str(df['Date of Birth_NE'][row])[:10])
				
				obj.age=df['Age_EN'][row]
				obj.age_ne_NP=df['Age_NE'][row]
				obj.mothers_name=df["Mother's.Name_EN"][row]
				obj.mothers_name_ne_NP=df["Mother's.Name_NE"][row]
				obj.fathers_name=df["Father's.Name_EN"][row]
				obj.fathers_name_ne_NP=df["Father's.Name_NE"][row]
				obj.marital_status=df['Maritial.Status_EN'][row]
				obj.marital_status_ne_NP=df['Maritial.Status_NE'][row]
				obj.husbands_name=df["Spouse's.Name_EN"][row]
				obj.husbands_name_ne_NP=df["Spouse's.Name_NE"][row]
				obj.caste=df['Ethnicity_EN'][row]
				obj.caste_ne_NP=df['Ethnicity_NE'][row]
				obj.mother_tongue=df['Mother.Tongue_EN'][row]
				obj.mother_tongue_ne_NP=df['Mother.Tongue_NE'][row]
				obj.educational_qualification=df['Formal.Education_EN'][row]
				obj.educational_qualification_ne_NP=df['Formal.Education_NE'][row]
				obj.subject=df['Degree.Name_EN'][row]
				obj.subject_ne_NP=df['Degree.Name_NE'][row]
				obj.permanent_address=df['Address (Permanent: District)_EN'][row]
				obj.permanent_address_ne_NP=df['Address (Permanent: District)_NE'][row]
				obj.permanent_gapa_napa=df['Village / Municipality / Sub-Metropolitan Municipality_EN'][row]
				obj.permanent_gapa_napa_ne_NP=df['Village / Municipality / Sub-Metropolitan Municipality_NE'][row]
				obj.permanent_ward_no=df['Ward_EN'][row]
				obj.permanent_ward_no_ne_NP=df['Ward_NE'][row]
				obj.permanent_tole=df['Street_EN'][row]
				obj.permanent_tole_ne_NP=df['Street_NE'][row]
				obj.temporary_address=df['Address (Temporary: District)_EN'][row]
				obj.temporary_address_ne_NP=df['Address (Temporary: District)_NE'][row]
				obj.temporary_gapa_napa=df['Temporary_Village / Municipality / Sub-Metropolitan Municipality_EN'][row]
				obj.temporary_gapa_napa_ne_NP=df['Temporary_Village / Municipality / Sub-Metropolitan Municipality_NE'][row]
				obj.temporary_ward_no=df['Temporary_Ward_EN'][row]
				obj.temporary_ward_no_ne_NP=df['Temporary_Ward_NE'][row]
				obj.temporary_tole=df['Temporary_Street_EN'][row]
				obj.temporary_tole_ne_NP=df['Temporary_Street_NE'][row]
				obj.mobile=df['Mobile_EN'][row]
				obj.mobile_ne_NP=df['Mobile_NE'][row]
				obj.contact_number=df['Contact.No_EN'][row]
				obj.contact_number_ne_NP=df['Contact.No_EN'][row]
				obj.email=df['Email'][row]
				obj.social_networking_medium=df['Social Media_EN'][row]
				obj.nirwachit_prakriya=df['Election.Type_EN'][row]
				obj.nirwachit_prakriya_ne_NP=df['Election.Type_NE'][row]
				obj.nirwachit_padh=df['Elected.Post_EN'][row]
				obj.nirwachit_padh_ne_NP=df['Elected.Post_NE'][row]
				obj.pichidiyeko_chhetra_ho_hoina=df['Is your area listed in Government of Nepal’s backward area?_EN'][row]
				obj.pichidiyeko_chhetra_ho_hoina_ne_NP=df['Is your area listed in Government of Nepal’s backward area?_NE'][row]
				obj.nirwachit_chhetrako_bibaran=df['Description of Elected Area_EN'][row]
				obj.nirwachit_chhetrako_bibaran_ne_NP=df['Description of Elected Area_NE'][row]
				obj.nirwachit_vayeko_chhetra_aafno_thegana=df['Is the elected constituency different than the address of the representative (Yes/No)?_EN'][row]
				obj.nirwachit_vayeko_chhetra_aafno_thegana_ne_NP=df['Is the elected constituency different than the address of the representative (Yes/No)?_NE'][row]
				obj.party_name=df['Name.of.Party_EN'][row]
				obj.party_name_ne_NP=df['Name.of.Party_NE'][row]
				obj.party_joined_date=df['Date.of.affiliation.with.Party_EN'][row]
				obj.party_joined_date_ne_NP=df['Date.of.affiliation.with.Party_NE'][row]
				obj.pramukh_jimmewari=df['Major.Respnsibility_EN'][row]
				obj.pramukh_jimmewari_ne_NP=df['Major.Respnsibility_NE'][row]
				obj.nirwachit_chetra_pratiko_pratibadhata=df['Political.Commitment_EN'][row]
				obj.nirwachit_chetra_pratiko_pratibadhata_ne_NP=df['Political.Commitment_NE'][row]
				obj.aaja_vanda_agadi_chunab_ladnu_vayeko_chha=df['Have.you.participated.in.an.election.before?_EN'][row]
				obj.aaja_vanda_agadi_chunab_ladnu_vayeko_chha_ne_NP=df['Have.you.participated.in.an.election.before?_NE'][row]
				obj.prapta_maat_sankhya=df['Number.of.votes.received_EN'][row]
				obj.prapta_maat_sankhya_ne_NP=df['Number.of.votes.received_NE'][row]
				obj.samlagna_sang_sastha_samuha=df['Details.of.the.recent.union, organization, group.you.are.engaged.with?_EN'][row]
				obj.samlagna_sang_sastha_samuha_ne_NP=df['Details.of.the.recent.union, organization, group.you.are.engaged.with?_NE'][row]
				obj.samitima_vumika=df['Role.in.organization_EN'][row]
				obj.samitima_vumika_ne_NP=df['Role.in.organization_NE'][row]
				obj.save()
		messages.success(request, 'Successfully loaded data from files')
		return HttpResponseRedirect('/cms/province-upload')
	except Exception as e:
		print(e.__class__.__name__ + " " + str(e))
		messages.error(request, "File Format not supported")
		return HttpResponseRedirect('/cms/province-upload')


class UserProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = User
	context_object_name = 'user'
	template_name = 'core/user_profile.html'

	def test_func(self):
		return self.request.user.is_superuser


class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = User
	fields = ('first_name', 'last_name', 'email')
	context_object_name = 'user'
	template_name = 'core/user_profile_update.html'

	def test_func(self):
		return self.request.user.is_superuser

	def get_success_url(self):
		success_url = reverse_lazy('core:user_profile', args=(self.object.pk,))
		return success_url