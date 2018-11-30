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

import numpy as np

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


class MapViewSet(views.APIView):

    def get(self, request):
        maps = {}
        nat = []
        province = []
        fed = []
        loc = []
        prov = {}

        local = MahilaPratinidhiForm.objects.values('province_id')\
        .annotate(Count('province_id'))\
        .annotate(total=Count('id')).order_by('province_id')

        national = RastriyaShava.objects.values('province_id')\
        .annotate(Count('province_id'))\
        .annotate(total=Count('id')).order_by('province_id')

        provincial = ProvinceMahilaPratinidhiForm.objects.values('province_id')\
        .annotate(Count('province_id'))\
        .annotate(total=Count('id')).order_by('province_id')

        federal = PratinidhiShava.objects.values('province_id')\
        .annotate(Count('province_id'))\
        .annotate(total=Count('id')).order_by('province_id')

        for item in local:
            loc.append(item['total'])
        
        maps['local']=loc

        for item in national:
            nat.append(item['total'])
        
        maps['national']=nat

        for item in provincial:
            province.append(item['total'])

        maps['provincial']=province
        
        for item in federal:
            fed.append(item['total'])

        maps['federal']=fed
            
        return Response(maps)


class AgeViewSet(views.APIView):
    def get(self, request):
        provinces_avg_age = {}
        age=[]
        sub_ranges = []
        ranges = []
        rastriya_age = RastriyaShava.objects.values('age')
        pratinidhi_age = PratinidhiShava.objects.values('age')
        provincial_age = ProvinceMahilaPratinidhiForm.objects.values('age')
        # local_age = MahilaPratinidhiForm.objects.values('age')
        

        ages = list(chain(rastriya_age, pratinidhi_age, provincial_age))

        lists = 20
        while lists < 100:
            sub_lists = lists 
            sub_ranges.append(sub_lists)
            while sub_lists <= lists:
                sub_lists = sub_lists + 5
                sub_ranges.append(sub_lists)
            ranges.append(sub_ranges)
            lists = lists + 5

        print(ranges)

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

        ethnicity.fromkeys({"caste"})

        #for total ethnicities
        pratinidhi_caste = PratinidhiShava.objects.all()
        provincial_caste = ProvinceMahilaPratinidhiForm.objects.all()

        castes = list(chain(pratinidhi_caste, provincial_caste))
        totals = []
        for caste in castes:
            totals.append(caste.caste)
                
        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        
        for total in total_arrays:
            ethnicity['caste'] = total[0]
            ethnicity['total'] = total[1]

            data.append(dict(ethnicity))

        total_ethnicity['total_ethnicity'] = data

        #for ethnicities on basis of provinces
        province_caste = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'caste').distinct()\
        .annotate(total=Count('caste'))
        castes = []
        for provinces in province_caste:
            caste = provinces['caste']
            castes.append(caste)
        
        caste_set = set(castes)
        print(caste_set)

        province_ethinicity=[]
        province_dict = {}
        
        for caste in caste_set:
            province_dict['caste'] = caste
            for item in province_caste:
                if caste in item['caste']:
                    if str(item['province_id']) in province_dict:
                        province_dict[str(item['province_id'])] = province_dict[str(item['province_id'])] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']
            
            province_ethinicity.append(dict(province_dict))


        total_ethnicity['provincial_ethnicity'] = province_ethinicity
        
        #for ethnicities on basis of political parties
        province_party_caste = ProvinceMahilaPratinidhiForm.objects.values('party_name', 'caste').distinct()\
        .annotate(total=Count('caste'))
        pratinidhi_party_caste = PratinidhiShava.objects.values('party_name', 'caste').distinct()\
        .annotate(total=Count('caste'))

        party_caste = list(chain(province_party_caste, pratinidhi_party_caste))

        castes = []
        for item in party_caste:
            caste = item['caste']
            castes.append(caste)
        
        caste_set = set(castes)
        print(caste_set)

        party_ethinicity=[]
        party_dict = {}
        
        for caste in caste_set:
            party_dict['caste'] = caste
            for item in party_caste:
                if caste in item['caste']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']
            
            party_ethinicity.append(dict(party_dict))

        total_ethnicity['party_ethnicity'] = party_ethinicity


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


class PoliticalEngagementViewSet(views.APIView):

    def get(self, request):

        total = {}
        data =[]

        rastriya_engagement = RastriyaShava.objects.values('party_joined_date')
        federal_engagement = PratinidhiShava.objects.values('party_joined_date')
        provincial_engagement = ProvinceMahilaPratinidhiForm.objects.values('party_joined_date')
        # local_engagement = MahilaPratinidhiForm.objects.values('party_joined_date')

        lists = list(chain(rastriya_engagement, federal_engagement, provincial_engagement))

        for item in lists:
            if item['party_joined_date'] != " ":
                data.append(2075 - int(item['party_joined_date'].replace(".0", "")))
        
        provinces = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'party_joined_date')\
        .annotate(Count('province_id'))

        total['total'] = data
        total['province_political_year'] = provinces
        total['rastriya_political_year'] = rastriya_engagement
        total['federal_political_year'] = federal_engagement

        return Response(total)





