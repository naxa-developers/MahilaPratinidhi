from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView, ListView
from core.models import *
from .forms import UserCreateForm
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import json
from django.core.mail import EmailMessage
from itertools import chain
from dal import autocomplete

from django.shortcuts import render
from django.db.models import Q
# from posts.models import Post


class Index(TemplateView):

    def get(self, request, *args, **kwargs):
        local_featured = MahilaPratinidhiForm.objects.filter(featured='True')[:1]
        national_featured = RastriyaShava.objects.filter(featured='True')[:1]
        pratinidhi_featured = PratinidhiShava.objects.filter(featured='True')[:1]
        provincial_featured = ProvinceMahilaPratinidhiForm.objects.filter(featured='True')[:1]
        featured_data = [local_featured, national_featured, pratinidhi_featured, provincial_featured]
        news = News.objects.all()

        images = BackgroundImage.objects.all()
        image_list = []

        for item in images:
            img = item.get_absolute_image_url()
            image_list.append(img)
        
        json_list = json.dumps(image_list)

        return render(request, 'public/index.html', {'featured_data': featured_data, 'news':news, 
        'image_list':json_list})


def signup(request):
    if request.GET.get('login'):
        return HttpResponseRedirect('/accounts/login/')
    else:
        if request.method == 'POST':
            signup_form = UserCreateForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('public/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf8'),
                'token': account_activation_token.make_token(user),
                })
                to_email = signup_form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            signup_form = UserCreateForm()
        return render(request, 'login.html', {'form':signup_form})
    


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect('/signup/')
    else:
        return HttpResponse('Activation link is invalid!')


class ExploreView(TemplateView):
    template_name = 'public/explore.html'


    def test_func(self):
        return not self.request.user.is_superuser


    def get(self, request, *args, **kwargs):
        names = {}
        name_list = []
        district = District.objects.all()
        rastriyas = RastriyaShava.objects.all()
        pratinidhis = PratinidhiShava.objects.all()
        provinces = Province.objects.all()

        province_names = ProvinceMahilaPratinidhiForm.objects.all()
        local_names = MahilaPratinidhiForm.objects.all()

        object_list = list(chain(rastriyas, pratinidhis, province_names, local_names))

        for lists in object_list:
            try:
                names['name']=lists.english_name
            except:
                names['name'] = lists.name

            names['id']=lists.pk
            names['models']=lists.__class__.__name__
            try:
                names['province_id']=lists.province_id
                names['district']=lists.district_id

            except:
                pass
            name_list.append(dict(names))

        # for lists in local_names:
        #     names.append(lists.name)
        json_list = json.dumps(name_list)
        # print(json_list)

        clicked = self.kwargs.get('clicked')
        return render(request, self.template_name, {'districts':district, 'rastriyas':rastriyas,
        'pratinidhis':pratinidhis, 'provinces':provinces, 'clicked':clicked, 'names':json_list})


class MahilaPratinidhiView(TemplateView):
    template_name = 'public/lists.html'

    def get(self, request, *args, **kwargs):
        names = {}
        name_list = []
        district = District.objects.all()

        local_names = MahilaPratinidhiForm.objects.filter(district_id=self.kwargs.get('district_id'))

        for lists in local_names:
            try:
                names['name'] = lists.english_name
            except:
                names['name'] = lists.name

            names['id'] = lists.pk
            names['models'] = lists.__class__.__name__
            try:
                names['district'] = lists.district_id

            except:
                pass
            name_list.append(dict(names))

        json_list = json.dumps(name_list)

        forms = MahilaPratinidhiForm.objects.filter(district_id=self.kwargs.get('district_id'))
        district_id = self.kwargs.get('district_id')
        return render(request, self.template_name, {'forms':forms, 'district_id':district_id, 'districts':district, 'names':json_list})


class LocalMahilaPratinidhiDetail(DetailView):
    template_name = 'public/detail.html'

    def get(self, request, *args, **kwargs):
        form = MahilaPratinidhiForm.objects.get(id=self.kwargs.get('pk'))
        return render(request, self.template_name, {'form':form})


class ProvinceView(ListView):
    template_name = "public/lists.html"
    
    def get(self, request, *args, **kwargs):
        names = {}
        name_list = []
        provinces = Province.objects.all()

        province_names = ProvinceMahilaPratinidhiForm.objects.filter(province_id=self.kwargs.get('province_id'))

        for lists in province_names:
            try:
                names['name'] = lists.english_name
            except:
                names['name'] = lists.name

            names['id'] = lists.pk
            names['models'] = lists.__class__.__name__
            try:
                names['province_id'] = lists.province_id

            except:
                pass
            name_list.append(dict(names))
        json_list = json.dumps(name_list)
        clicked = self.kwargs.get('clicked')
        forms = ProvinceMahilaPratinidhiForm.objects.filter(province_id=self.kwargs.get('province_id'))
        province_id = self.kwargs.get('province_id')
        return render(request, self.template_name, {'forms': forms, 'province_id':province_id, 'provinces':provinces, 'names':json_list, 'clicked':clicked})


class ProvincialMahilaPratinidhiDetail(DetailView):
    template_name = 'public/detail.html'

    def get(self, request, *args, **kwargs):
        form = ProvinceMahilaPratinidhiForm.objects.get(id=self.kwargs.get('pk'))
        return render(request, self.template_name, {'form':form})


class MahilaDetail(DetailView):
    template_name = 'public/detail.html'

    def get(self, request, *args, **kwargs):
        if RastriyaShava.objects.filter(id=self.kwargs.get('pk')):
            form = RastriyaShava.objects.get(id=self.kwargs.get('pk'))

        elif PratinidhiShava.objects.filter(id=self.kwargs.get('pk')):
            form = PratinidhiShava.objects.get(id=self.kwargs.get('pk'))

        elif ProvinceMahilaPratinidhiForm.objects.filter(id=self.kwargs.get('pk')):
            form = ProvinceMahilaPratinidhiForm.objects.get(id=self.kwargs.get('pk'))

        else:
            form = MahilaPratinidhiForm.objects.get(id=self.kwargs.get('pk'))
        
        return render(request, self.template_name, {'form':form})


class RastriyaMahilaDetail(TemplateView):
    template_name = 'public/detail.html'

    def get(self, request, *args, **kwargs):
        form = RastriyaShava.objects.get(id=self.kwargs.get('pk'))
        return render(request, self.template_name, {'form':form})


class PratinidhiMahilaDetail(DetailView):
    template_name = 'public/detail.html'

    def get(self, request, *args, **kwargs):
        form = PratinidhiShava.objects.get(id=self.kwargs.get('pk'))
        return render(request, self.template_name, {'form':form})


class DataVisualize(TemplateView):
    template_name = 'public/data.html'


    def get(self, request, *args, **kwargs):
        # local = MahilaPratinidhiForm.objects.all()
        national = RastriyaShava.objects.all()
        pratinidhi = PratinidhiShava.objects.all()
        provincial = ProvinceMahilaPratinidhiForm.objects.all()
        # total = local.count() + national.count() + pratinidhi.count() + provincial.count()
        total = national.count() + pratinidhi.count() + provincial.count()


        married = 0
        graduate = 0
        direct = 0

        # for mahila in local:
        #     if mahila.marital_status == 'Married' or mahila.marital_status == 'विवाहित':
        #         married = married + 1
            
        #     if mahila.educational_qualification == 'Graduate' or 'स्नातक' in mahila.educational_qualification:
        #         graduate = graduate + 1
            
        for mahila in national:
            if mahila.marital_status == 'Married' or mahila.marital_status == 'विवाहित':
                married = married + 1
            
            if mahila.educational_qualification == 'Graduate':
                graduate = graduate + 1
            
            if mahila.nirwachit_prakriya == 'Directly Elected':
                direct = direct + 1
            
        for mahila in pratinidhi:
            if mahila.marital_status == 'Married' or mahila.marital_status == 'विवाहित':
                married = married + 1
            
            if mahila.educational_qualification == 'Graduate':
                graduate = graduate + 1
            
            if mahila.nirwachit_prakriya == 'Directly Elected':
                direct = direct + 1
        
        for mahila in provincial:
            if mahila.marital_status == 'Married' or mahila.marital_status == 'विवाहित':
                married = married + 1
            
            if mahila.educational_qualification == 'Graduate':
                graduate = graduate + 1
            
            if mahila.nirwachit_prakriya == 'Directly Elected':
                direct = direct + 1

        return render(request, self.template_name, {'total':total, 'married':married, 'graduate':graduate, 'direct':direct})
    

class NewsView(TemplateView):
    template_name = 'public/news-detail.html'

    def get(self, request, *args, **kwargs):
        news = News.objects.get(id=self.kwargs.get('pk'))
        latest_news = News.objects.latest()
        print(latest_news)
        return render(request, self.template_name, {'news':news, 'latest_news': latest_news})


def read_view(request, ):
    try:
        with open('C:/gitnaxa/work/Mahila-Pratinidhi/CV_Akshya_Kumar_Shrestha.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'filename=some_file.pdf'
        
        return response
    except:
        msg = "There is no file"
        return HttpResponse(msg)


class Detail(TemplateView):
    template_name = 'public/lists.html'


def callRequestView(request, *args, **kwargs):
    if RastriyaShava.objects.get(pk=kwargs.get('pk')):
        mahila = RastriyaShava.objects.get(pk=kwargs.get('pk'))

    elif PratinidhiShava.objects.get(pk=kwargs.get('pk')):
        mahila = PratinidhiShava.objects.get(pk=kwargs.get('pk'))

    elif ProvinceMahilaPratinidhiForm.objects.get(pk=kwargs.get('pk')):
        mahila = ProvinceMahilaPratinidhiForm.objects.get(pk=kwargs.get('pk'))

    else:
        mahila = MahilaPratinidhiForm.objects.get(pk=kwargs.get('pk'))


    if request.user.is_authenticated:
        email = EmailMessage('Call Request', request.user.username+"has made call request to "+ mahila.name ,
                                         to=['akshya.shrestha7402@gmail.com'])
        email.send()
        return HttpResponseRedirect('/explore/general')
    else:
        print("Please login first!")
        return render(request, "login.html")




# class NameAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         qs = RastriyaShava.objects.all()
#
#         if self.q:
#             qs = qs.filter(english_name_istartswith=self.q)
#
#         return qs







# class SearchDetail(DetailView):
#     template_name = 'public/detail.html'

#     def get(self, request, *args, **kwargs):
#         rastriya = RastriyaShava.objects.filter(english_name=self.kwargs.get('english_name'))
#         return render(request, self.template_name, {'form': rastriya})


# class searchView(ListView):
#     template_name = 'public/lists.html'

#     def get(self, request, *args, **kwargs):
#         print("dasda")
#         name = self.request.GET.get('search')
#         print("hello" + name)

#         national = RastriyaShava.objects.filter(name = name)
#         province = ProvinceMahilaPratinidhiForm.objects.filter(name__icontains = name)
#         federal = PratinidhiShava.objects.filter(name__icontains = name)
#         local = MahilaPratinidhiForm.objects.filter(name__icontains = name)

#         model = list(chain(national, province, federal, local))

#         if national is not None:
#             return render(self.request, self.template_name, {'forms': model})


# def searchposts(request):
#     if request.method == 'GET':
#         query= request.GET.get('q')


#         submitbutton= request.GET.get('submit')

#         if query is not None:
#             print("entered")
#             lookups= Q(english_name__icontains=query)
#             print(lookups)
#             rastriya = RastriyaShava.objects.filter(lookups)
#             pratinidhi = PratinidhiShava.objects.filter(lookups)
#             province = ProvinceMahilaPratinidhiForm.objects.filter(lookups)
#             locals = MahilaPratinidhiForm.objects.filter(Q(name__icontains=query))
#             results = list(chain(rastriya, pratinidhi, province))
#             print("end")
#             context={'results': results, 'locals': locals,
#                      'submitbutton': submitbutton}

#             return render(request, 'public/search.html', context)

#         else:
#             return render(request, 'public/explore.html')

#     else:
#         return render(request, 'public/explore.html')

