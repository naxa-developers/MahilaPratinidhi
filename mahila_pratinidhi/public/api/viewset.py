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

        total_ages = {}
        data = []
        ranges = []
        rastriya_age = RastriyaShava.objects.values('age', 'province_id', 'party_name')
        pratinidhi_age = PratinidhiShava.objects.values('age', 'province_id', 'party_name')
        provincial_age = ProvinceMahilaPratinidhiForm.objects.values('age', 'province_id', 'party_name')
        # local_age = MahilaPratinidhiForm.objects.values('age')
        
        # for total age groups
        ages = list(chain(rastriya_age, pratinidhi_age, provincial_age))

        lists = 20
        while lists < 100:
            sub_ranges = []
            sub_lists = lists 
            sub_ranges.append(sub_lists)
            while sub_lists <= lists:
                sub_lists = sub_lists + 5
                sub_ranges.append(sub_lists)
            ranges.append(sub_ranges)
            lists = lists + 5


        range_list = []

        for age_range in ranges:
            r = range(age_range[0], age_range[1])
            for age in ages:
                if age['age'] in r:
                    range_list.append(str(age_range[0]) + "-" + str(age_range[1]))

        total_arrays = np.array(np.unique(range_list, return_counts=True)).T
        age_dict = {}
        for total in total_arrays:
            age_dict['label'] = total[0]
            age_dict['total'] = total[1]
            data.append(dict(age_dict))

        total_ages['age_total'] = data
        
        #for ages per provinces
        province_age = []
        for age_range in ranges:
            age_dict = {}
            count = 0
            r = range(age_range[0], age_range[1])
            age_dict["label"] = str(age_range[0]) + "-" + str(age_range[1])
            for age in provincial_age:
                if age['age'] in r:
                    count = count + 1
                    age_dict[age['province_id']] = count + 1
               
            province_age.append(dict(age_dict))

        total_ages['province_age'] = province_age

        # for ages per party
        age_list = list(chain(provincial_age, pratinidhi_age))

        party_age = []
        for age_range in ranges:
            age_dict = {}
            count = 0
            r = range(age_range[0], age_range[1])
            age_dict["label"] = str(age_range[0]) + "-" + str(age_range[1])
            for age in age_list:
                if age['age'] in r:
                    count = count + 1
                    age_dict[age['party_name']] = count + 1
               
            party_age.append(dict(age_dict))

        total_ages['age_per_party'] = party_age


        return Response(total_ages)


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

        province_ethinicity=[]
        
        
        for caste in caste_set:
            province_dict = {}
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

        party_ethinicity=[]
        
        for caste in caste_set:
            party_dict = {}
            party_dict['caste'] = caste
            for item in party_caste:
                if caste in item['caste']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']
            
            party_ethinicity.append(dict(party_dict))

        total_ethnicity['party_ethnicity'] = party_ethinicity
        
        return Response(total_ethnicity)


class MotherTongueViewSet(views.APIView):
    
    def get(self, request):

        total_mother_tongue = {}
        data = []
        mother_tongue={}

        #for total mother_tongues
        pratinidhi_lang = PratinidhiShava.objects.all()
        provincial_lang = ProvinceMahilaPratinidhiForm.objects.all()

        languages = list(chain(pratinidhi_lang, provincial_lang))
        totals = []
        for language in languages:
            totals.append(language.mother_tongue)
        
        total_arrays = np.array(np.unique(totals, return_counts=True)).T
        
        for total in total_arrays:
            mother_tongue['mother_tongue'] = total[0]
            mother_tongue['total'] = total[1]

            data.append(dict(mother_tongue))

        total_mother_tongue['total_mother_tongue'] = data

        #for mother_tongue on basis of provinces
        province_mother_tongue = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'mother_tongue')\
        .distinct().annotate(total=Count('mother_tongue'))
        languages = []
        for language in province_mother_tongue:
            lang = language['mother_tongue']
            languages.append(lang)
        
        language_set = set(languages)

        province_language=[]
        
        
        for language in language_set:
            province_dict = {}
            province_dict['mother_tongue'] = language
            for item in province_mother_tongue:
                if language in item['mother_tongue']:
                    if str(item['province_id']) in province_dict:
                        province_dict[str(item['province_id'])] = province_dict[str(item['province_id'])] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']
            
            province_language.append(dict(province_dict))


        total_mother_tongue['provincial_mother_tongue'] = province_language
        
        #for mother tongue on basis of political parties
        province_party_lang = ProvinceMahilaPratinidhiForm.objects.values('party_name', 'mother_tongue')\
        .distinct().annotate(total=Count('mother_tongue'))
        pratinidhi_party_lang = PratinidhiShava.objects.values('party_name', 'mother_tongue')\
        .distinct().annotate(total=Count('mother_tongue'))

        party_lang = list(chain(province_party_lang, pratinidhi_party_lang))

        languages = []
        for item in party_lang:
            lang = item['mother_tongue']
            languages.append(lang)
        
        language_set = set(languages)

        party_language=[]
        
        for language in language_set:
            party_dict = {}
            party_dict['mother_tongue'] = language
            for item in party_lang:
                if language in item['mother_tongue']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']
            
            party_language.append(dict(party_dict))

        total_mother_tongue['party_mother_tongue'] = party_language
        
        return Response(total_mother_tongue)

class EducationViewSet(views.APIView):

   def get(self, request):

        total_education = {}
        data = []
        edu={}

        #for total educational qualification
        pratinidhi_education = PratinidhiShava.objects.all()
        provincial_education = ProvinceMahilaPratinidhiForm.objects.all()

        educations = list(chain(pratinidhi_education, provincial_education))
        totals = []
        for education in educations:
            totals.append(education.educational_qualification)
        
        total_arrays = np.array(np.unique(totals, return_counts=True)).T
        
        for total in total_arrays:
            edu['education'] = total[0]
            edu['total'] = total[1]

            data.append(dict(edu))

        total_education['total_education'] = data

        #for educational qualification on basis of provinces
        province_education = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'educational_qualification')\
        .distinct().annotate(total=Count('educational_qualification'))
        educations = []
        for education in province_education:
            edu = education['educational_qualification']
            educations.append(edu)
        
        education_set = set(educations)

        province_edu=[]
        
        
        for education in education_set:
            province_dict = {}
            province_dict['education'] = education
            for item in province_education:
                if education in item['educational_qualification']:
                    if str(item['province_id']) in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']
            
            province_edu.append(dict(province_dict))


        total_education['provincial_education'] = province_edu
        
        #for ethnicities on basis of political parties
        province_party_edu = ProvinceMahilaPratinidhiForm.objects.values('party_name', 'educational_qualification')\
        .distinct().annotate(total=Count('educational_qualification'))
        pratinidhi_party_edu = PratinidhiShava.objects.values('party_name', 'educational_qualification')\
        .distinct().annotate(total=Count('educational_qualification'))

        party_edu = list(chain(province_party_edu, pratinidhi_party_edu))

        educations = []
        for item in party_edu:
            edu = item['educational_qualification']
            educations.append(edu)
        
        education_set = set(educations)

        party_education=[]
        
        for education in education_set:
            party_dict = {}
            party_dict['educational_qualification'] = education
            for item in party_edu:
                if education in item['educational_qualification']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']
            
            party_education.append(dict(party_dict))

        total_education['party_educational_qualification'] = party_education
        
        return Response(total_education)


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





