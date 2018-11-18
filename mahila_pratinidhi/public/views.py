from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView, ListView
from core.models import *
from .forms import UserCreateForm


class Index(TemplateView):
    template_name="/"

    def get(self, request, *args, **kwargs):
        featured_data = MahilaPratinidhiForm.objects.all()[:9]
        news = News.objects.all()
        image_list = list(BackgroundImage.objects.all())

        if self.request.user.is_superuser:
            return render(request, self.template_name)
        else:
            return render(request, 'public/index.html', {'featured_data': featured_data, 'news':news, 
            'image_list':image_list})


class SignUp(CreateView):
    form_class = UserCreateForm
    template_name="public/signup.html"
    success_url = reverse_lazy('login')


class ExploreView(TemplateView):
    template_name = 'public/explore.html'


    def test_func(self):
        return not self.request.user.is_superuser


    def get(self, request, *args, **kwargs):
        district = District.objects.all()
        rastriyas = RastriyaShava.objects.all()
        pratinidhis = PratinidhiShava.objects.all()
        provinces = Province.objects.all()
        return render(request, self.template_name, {'districts':district, 'rastriyas':rastriyas,
        'pratinidhis':pratinidhis, 'provinces':provinces})


class MahilaPratinidhiView(TemplateView):
    template_name = 'public/lists.html'


    def get(self, request, *args, **kwargs):
        forms = MahilaPratinidhiForm.objects.filter(district_id=self.kwargs.get('district_id'))
        return render(request, self.template_name, {'forms':forms})


class ProvinceView(TemplateView):
    template_name = "public/lists.html"

    def get(self, request, *args, **kwargs):
        forms = ProvinceMahilaPratinidhiForm.objects.filter(province_id=self.kwargs.get('province_id'))
        return render(request, self.template_name, {'forms': form})

class Detail(DetailView):
    model = MahilaPratinidhiForm
    template_name = 'public/detail.html'
    context_object_name = 'form'

    


class DataVisualize(UserPassesTestMixin, TemplateView):
    template_name = 'public/data.html'


    def test_func(self):
        return not self.request.user.is_superuser


    def get(self, request, *args, **kwargs):
        form = MahilaPratinidhiForm.objects.all()
        total = form.count
        married = MahilaPratinidhiForm.objects.filter(marital_status='ljjflxt').count
        graduate = MahilaPratinidhiForm.objects.filter(educational_qualification__contains=':gfts').count
        return render(request, self.template_name, {'total':total, 'married':married, 'graduate':graduate})
    

class List(UserPassesTestMixin, TemplateView):
    template_name = 'public/lists.html'


    def test_func(self):
        return not self.request.user.is_superuser
    

class Tab(UserPassesTestMixin, TemplateView):
    template_name = 'public/tab.html'


    def test_func(self):
        return not self.request.user.is_superuser


