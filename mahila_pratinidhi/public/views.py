from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
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
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
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
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreateForm()
    return render(request, 'public/signup.html', {'form': form})


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
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class ExploreView(TemplateView):
    template_name = 'public/explore.html'


    def test_func(self):
        return not self.request.user.is_superuser


    def get(self, request, *args, **kwargs):
        names = []
        district = District.objects.all()
        rastriyas = RastriyaShava.objects.all()
        pratinidhis = PratinidhiShava.objects.all()
        provinces = Province.objects.all()

        province_names = ProvinceMahilaPratinidhiForm.objects.all()
        local_names = MahilaPratinidhiForm.objects.all()

        object_list = list(chain(rastriyas, pratinidhis, province_names))

        for lists in object_list:

            names.append(lists.english_name)

        # for lists in local_names:
        #     names.append(lists.name)
        # print(names)
        json_list = json.dumps(names)

        clicked = self.kwargs.get('clicked')
        return render(request, self.template_name, {'districts':district, 'rastriyas':rastriyas,
        'pratinidhis':pratinidhis, 'provinces':provinces, 'clicked':clicked, 'names':json_list})


class MahilaPratinidhiView(TemplateView):
    template_name = 'public/lists.html'

    def get(self, request, *args, **kwargs):
        forms = MahilaPratinidhiForm.objects.filter(district_id=self.kwargs.get('district_id'))
        district_id = self.kwargs.get('district_id')
        return render(request, self.template_name, {'forms':forms, 'district_id':district_id})


class LocalMahilaPratinidhiDetail(DetailView):
    template_name = 'public/detail.html'

    def get(self, request, *args, **kwargs):
        form = MahilaPratinidhiForm.objects.get(id=self.kwargs.get('pk'))
        return render(request, self.template_name, {'form':form})


class ProvinceView(ListView):
    template_name = "public/lists.html"
    
    def get(self, request, *args, **kwargs):
        forms = ProvinceMahilaPratinidhiForm.objects.filter(province_id=self.kwargs.get('province_id'))
        province_id = self.kwargs.get('province_id')
        return render(request, self.template_name, {'forms': forms, 'province_id':province_id})


class ProvincialMahilaPratinidhiDetail(DetailView):
    template_name = 'public/detail.html'

    def get(self, request, *args, **kwargs):
        form = ProvinceMahilaPratinidhiForm.objects.get(id=self.kwargs.get('pk'))
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
        local = MahilaPratinidhiForm.objects.all()
        national = RastriyaShava.objects.all()
        pratinidhi = PratinidhiShava.objects.all()
        provincial = ProvinceMahilaPratinidhiForm.objects.all()
        total = local.count() + national.count() + pratinidhi.count() + provincial.count()

        married = 0
        graduate = 0
        direct = 0

        for mahila in local:
            if mahila.marital_status == 'ljjflxt':
                married = married + 1
            
            if ':gfts' in mahila.educational_qualification:
                graduate = graduate + 1
            
        for mahila in national:
            if mahila.marital_status == 'विवाहित':
                married = married + 1
            
            if 'स्नात' in mahila.educational_qualification:
                graduate = graduate + 1
            
            if 'प्रत्यक्ष' in mahila.nirwachit_prakriya:
                direct = direct + 1
            
        for mahila in pratinidhi:
            if mahila.marital_status == 'विवाहित':
                married = married + 1
            
            if 'स्नात' in mahila.educational_qualification:
                graduate = graduate + 1
            
            if 'प्रत्यक्ष' in mahila.nirwachit_prakriya:
                direct = direct + 1
        
        for mahila in provincial:
            if mahila.marital_status == 'विवाहित':
                married = married + 1
            
            if 'स्नात' in mahila.educational_qualification:
                graduate = graduate + 1
            
            if 'प्रत्यक्ष' in mahila.nirwachit_prakriya:
                direct = direct + 1

        return render(request, self.template_name, {'total':total, 'married':married, 'graduate':graduate, 'direct':direct})
    

class NewsView(TemplateView):
    template_name = 'public/news-detail.html'

    def get(self, request, *args, **kwargs):
        news = News.objects.get(id=self.kwargs.get('pk'))
        latest_news = News.objects.latest
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

class callRequestView(TemplateView):
    template_name = 'public/signup.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated():
                email = EmailMessage('Call Request', 'This user has made the call request.',
                                         to=['akshya.shrestha7402@gmail.com'])
                email.send()
        except:
            print("Please login first!")
        return render(request, self.template_name)

class SearchDetail(DetailView):
    template_name = 'public/detail.html'

    def get(self, request, *args, **kwargs):
        rastriya = RastriyaShava.objects.filter(english_name=self.kwargs.get('english_name'))
        return render(request, self.template_name, {'form': rastriya})


# class searchView(ListView):
#     template_name = 'public/lists.html'
#     print('hellooo')
#
#     def get(self, request, *args, **kwargs):
#         print("dasda")
#         name = self.request.GET.get('search')
#         print("hello" + name)
#
#         national = RastriyaShava.objects.filter(name = name)
#         province = ProvinceMahilaPratinidhiForm.objects.filter(name__icontains = name)
#         federal = PratinidhiShava.objects.filter(name__icontains = name)
#         local = MahilaPratinidhiForm.objects.filter(name__icontains = name)
#
#         model = list(chain(national, province, federal, local))
#
#         if national is not None:
#             return render(self.request, self.template_name, {'forms': model})

# def searchposts(request):
#     print("hello")
#     if request.method == 'GET':
#         query= request.GET.get('q')
#
#
#         submitbutton= request.GET.get('submit')
#
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
#
#             return render(request, 'public/search.html', context)
#
#         else:
#             return render(request, 'public/explore.html')
#
#     else:
#         return render(request, 'public/explore.html')

