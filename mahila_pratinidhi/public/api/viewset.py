from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import status, serializers, views
from rest_framework.response import Response
import json
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from itertools import chain

from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from .serializers import RastriyaShavaSerializer, ProvinceSerializer, LocalMahilaSerializer, PratinidhiShavaSerializer, AgeSerializers
from core.models import RastriyaShava, PratinidhiShava, ProvinceMahilaPratinidhiForm, MahilaPratinidhiForm
from django.db.models import Avg, Count, Sum

@api_view(['GET'])
def country_geojson(request):

    data = {}
    try:
        with open('jsons/province.json') as f:
            data = json.load(f)
    except:
        pass

    return Response(data)


@api_view(['GET'])
def province_geojson(request, province_id):

    data = {}
    try:
        with open('jsons/province/{}.json'.format(province_id)) as f:
            data = json.load(f)
    except:
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    return Response(data)


@api_view(['GET'])
def gapanapa_geojson(request, district):

    data = {}
    try:
        with open('jsons/gapanapa/{}.geojson'.format(district)) as f:
            data = json.load(f)
    except:
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    return Response(data)


class RastriyaViewSet(ReadOnlyModelViewSet):
    queryset = RastriyaShava.objects.all()
    serializer_class = RastriyaShavaSerializer


class AgeViewSet(views.APIView):
    def get(self, request):
        provinces_avg_age = {}
        age=[]
        rastriya_age = RastriyaShava.objects.values('age')
        pratinidhi_age = PratinidhiShava.objects.values('age')
        provincial_age = ProvinceMahilaPratinidhiForm.objects.values('age')
        # local_age = MahilaPratinidhiForm.objects.values('age')
        

        ages = list(chain(rastriya_age, pratinidhi_age, provincial_age))

        for ages in ages:
            if ages['age'] != "":
                age.append(ages['age'])
        
        provinces_avg_age = ProvinceMahilaPratinidhiForm.objects.values('province_id')\
        .annotate(Count('province_id'))\
        .annotate(age_avg=Avg('age'))

        province = ProvinceMahilaPratinidhiForm.objects.values('age')\
        .aggregate(age_avg=Avg('age'))

        national = RastriyaShava.objects.values('age')\
        .aggregate(age_avg=Avg('age'))

        federal = PratinidhiShava.objects.values('age')\
        .aggregate(age_avg=Avg('age'))

        data = {'total_age':age, 'provinces_average_age':provinces_avg_age, 
        'province':province, 'national':national,
        'federal':federal}
        return Response(data)


class EthnicityViewSet(views.APIView):
    def get(self, request):

        total_ethnicity = {}
        data = []
        ethnicity={}

        province_ethinicity=[]
        ethnicity.fromkeys({"caste"})
        print(ethnicity)

        # rastriya_caste = RastriyaShava.objects.values('caste').annotate(Count('caste'))\
        # .annotate(total=Sum('id'))

        pratinidhi_caste = PratinidhiShava.objects.values('caste').annotate(Count('caste'))\
        .annotate(total=Count('id'))

        provincial_caste = ProvinceMahilaPratinidhiForm.objects.values('caste').annotate(Count('caste'))\
        .annotate(total=Count('id'))
        # local_caste = MahilaPratinidhiForm.objects.values('caste')
        
        # for castes in rastriya_caste:
        #     if not castes['caste'] in ethnicity['caste']:
        #         ethnicity['caste']=castes['caste']
        #         ethnicity[castes['caste']]['total']=castes['total']
            
        #     else:
        #         ethnicity[castes['caste']]['total'] += castes['total']

        castes = list(chain(pratinidhi_caste, provincial_caste))

        for caste in castes:
            ethnicity['caste'] = caste['caste']
            ethnicity['total'] = caste['total']
            data.append(dict(ethnicity))
        
        #total ethnicities and their numbers
        total_ethnicity['total_ethnicity'] = data

        #total ethnicities with respect to province
        total_ethnicity['province_ethnicity'] = provincial_caste

        #total ethnicities with respect to federal states
        total_ethnicity['pratinidhi_ethnicity'] = pratinidhi_caste
        
        # for castes in rastriya_caste:
        #     if not castes['caste'] in ethnicity['caste']:
            #     ethnicity['caste']=castes['caste']
            #     ethnicity['total']=castes['total']
            
            # else:
            #     ethnicity['total'] += castes['total']

        
        return Response(total_ethnicity)


class MotherTongueViewSet(views.APIView):
    
    def get(self, request):

        total = {}
        lang = {}
        data = []

        pratinidhi_lang = PratinidhiShava.objects.values('mother_tongue').annotate(Count('mother_tongue'))\
        .annotate(total=Count('id'))

        provincial_lang = ProvinceMahilaPratinidhiForm.objects.values('mother_tongue')\
        .annotate(Count('mother_tongue'))\
        .annotate(total=Count('id'))

        languages = list(chain(pratinidhi_lang, provincial_lang))

        for language in languages:
            lang['mother_tongue'] = language['mother_tongue']
            lang['total'] = language['total']
            data.append(dict(lang))
        

        total['total_mother_tongues'] = data
        total['provincial_mother_tongue'] = provincial_lang
        total['pratinidhi_mother_tongue'] = pratinidhi_lang

        return Response(total)

class EducationViewSet(views.APIView):

    def get(self, request):

        total = {}
        data = []
        education = {}

        pratinidhi_edu = PratinidhiShava.objects.values('educational_qualification')\
        .annotate(Count('educational_qualification'))\
        .annotate(total=Count('id'))

        provincial_edu = ProvinceMahilaPratinidhiForm.objects.values('educational_qualification')\
        .annotate(Count('educational_qualification'))\
        .annotate(total=Count('id'))

        edu = list(chain(pratinidhi_edu, provincial_edu))

        for item in edu:
            education['education'] = item['educational_qualification']
            education['total'] = item['total']
            data.append(dict(education))

        total['total_education'] = data
        total['provincial_education'] = provincial_edu
        total['pratinidhi_education'] = pratinidhi_edu

        return Response(total)





