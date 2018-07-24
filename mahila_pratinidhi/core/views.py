from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView

from .models import MahilaPratinidhiForm, District
from .forms import MahilaPratinidhiFormForm


class MahilaPratinidhiFormCreateView(LoginRequiredMixin, CreateView):

	model = MahilaPratinidhiForm
	form_class = MahilaPratinidhiFormForm
	success_url = reverse_lazy('core:dashboard')
	template_name = "core/mahila_pratinidhi_form.html"


class Dashboard(LoginRequiredMixin, TemplateView):

	template_name = "core/dashboard.html"

	def get(self, request, *args, **kwargs):
		districts = District.objects.all()
		district = request.GET.get('dist')
		forms = MahilaPratinidhiForm.objects.all().select_related('district').filter(district__name=district)

		return render(request, self.template_name, {'forms': forms, 'districts': districts})


class MahilaPratinidhiFormDetailView(LoginRequiredMixin, DetailView):

	model = MahilaPratinidhiForm
	template_name = "core/mahila_pratinidhi_detail.html"
	context_object_name = 'form'


class MahilaPratinidhiFormUpdateView(LoginRequiredMixin, UpdateView):

	model = MahilaPratinidhiForm
	form_class = MahilaPratinidhiFormForm
	success_url = reverse_lazy('core:dashboard')
	template_name = "core/mahila_pratinidhi_form.html"


class MahilaPratinidhiFormDeleteView(LoginRequiredMixin, DeleteView):

	model = MahilaPratinidhiForm
	success_url = reverse_lazy('core:dashboard')
	template_name = "core/mahila_pratinidhi_delete.html"


def file_upload(request):
	import pandas as pd
	df = pd.read_excel(request.FILES['sentFile'])
	# paramFile = request.FILES['sentFile'].read()
	print(df.columns)



