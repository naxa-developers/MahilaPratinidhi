from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from .models import MahilaPratinidhiForm
from .forms import MahilaPratinidhiFormForm


class MahilaPratinidhiFormCreateView(CreateView):

	model = MahilaPratinidhiForm
	form_class = MahilaPratinidhiFormForm
	success_url = reverse_lazy('core:mahila_pratinidhi_list')
	template_name = "core/mahila_pratinidhi_form.html"


class MahilaPratinidhiFormListView(ListView):

	model = MahilaPratinidhiForm
	template_name = "core/mahila_pratinidhi_list.html"


class MahilaPratinidhiFormDetailView(DetailView):

	model = MahilaPratinidhiForm
	template_name = "core/mahila_pratinidhi_detail.html"


class MahilaPratinidhiFormUpdateView(UpdateView):

	model = MahilaPratinidhiForm
	form_class = MahilaPratinidhiFormForm
	success_url = reverse_lazy('core:mahila_pratinidhi_list')
	template_name = "core/mahila_pratinidhi_form.html"


class MahilaPratinidhiFormDeleteView(DeleteView):

	model = MahilaPratinidhiForm
	success_url = reverse_lazy('core:mahila_pratinidhi_list')
	template_name = "core/mahila_pratinidhi_delete.html"


