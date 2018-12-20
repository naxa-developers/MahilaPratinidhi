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
from .serializers import RastriyaShavaSerializer, ProvinceSerializer, LocalMahilaSerializer, \
PratinidhiShavaSerializer, AgeSerializers, DistrictsSerializer, HlcitSerializer
from core.models import RastriyaShava, PratinidhiShava, ProvinceMahilaPratinidhiForm, MahilaPratinidhiForm, Province, District
from django.db.models import Avg, Count, Sum

import numpy as np
import re

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
        map_api = {}

        total_list = []
        total_dict = {}
        national_dict = {}
        province_dict = {}
        local_dict = {}
        federal_dict = {}
        totals = []

        national_province = Province.objects.values('name').annotate(total=Count('rastriyashava'))
        for item in national_province:
            for i in range(item['total']):
                if item['name']:
                    totals.append(item['name'])

        federal_province = Province.objects.values('name').annotate(total=Count('pratinidhishava'))
        for item in federal_province:
            for i in range(item['total']):
                if item['name']:
                    totals.append(item['name'])
        
        #for local
        # local_province = Province.objects.values('name').annotate(total=Count('mahilapratinidhiform'))
        # for item in local_province:
        #     for i in range(item['total']):
        #         totals.append(item['name'])
        
        province_province = Province.objects.values('name').annotate(total=Count('province_mahila_pratinidhi_form'))
        for item in province_province:
            for i in range(item['total']):
                if item['name']:
                    totals.append(item['name'])
        
        total_arrays = np.array(np.unique(totals, return_counts=True)).T


        for total in total_arrays:
            total_dict[total[0]] = int(total[1])
        
        totals = []
        national_district = RastriyaShava.objects.values('permanent_address').annotate(total=Count('permanent_address'))
        for item in national_district:
            for i in range(item['total']):
                if item['permanent_address']:
                    totals.append(item['permanent_address'])

        federal_district = PratinidhiShava.objects.values('permanent_address').annotate(total=Count('permanent_address'))
        for item in federal_district:
            for i in range(item['total']):
                if item['permanent_address']:
                    totals.append(item['permanent_address'])
        
        province_district = ProvinceMahilaPratinidhiForm.objects.values('permanent_address').annotate(total=Count('permanent_address'))
        for item in province_district:
            for i in range(item['total']):
                if item['permanent_address']:
                    totals.append(item['permanent_address'])

        #for local
        # district_district = District.objects.values('name').annotate(total=Count('district'))
        # for item in district_district:
        #     for i in range(item['total']):
        #         totals.append(item['name'])
        
        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            total_dict[total[0]] = int(total[1])

        totals = []
        national_district = RastriyaShava.objects.values('hlcit_code').annotate(total=Count('hlcit_code'))
        for item in national_district:
            for i in range(item['total']):
                if item['hlcit_code']:
                    totals.append(item['hlcit_code'])

        federal_district = PratinidhiShava.objects.values('hlcit_code').annotate(total=Count('hlcit_code'))
        for item in federal_district:
            for i in range(item['total']):
                if item['hlcit_code']:
                    totals.append(item['hlcit_code'])
        
        province_district = ProvinceMahilaPratinidhiForm.objects.values('hlcit_code').annotate(total=Count('hlcit_code'))
        for item in province_district:
            for i in range(item['total']):
                if item['hlcit_code']:
                    totals.append(item['hlcit_code'])

        #for local
        # district_district = District.objects.values('hlcit_code').annotate(total=Count('hlcit_code'))
        # for item in district_district:
        #     for i in range(item['total']):
        #         totals.append(item['hlcit_code'])

        total_arrays = np.array(np.unique(totals, return_counts=True)).T
        
        for total in total_arrays:
            total_dict[total[0]] = int(total[1])
        
        total_list.append(total_dict)

        map_api['all']=total_list

        #for national lists
        national_list = []
        national_dict = {}

        national_province = Province.objects.values('name').annotate(total=Count('rastriyashava'))

        for item in national_province:
            if item['name']:
                national_dict[item['name']] = item['total']

        national_district = RastriyaShava.objects.values('permanent_address').\
        annotate(total=Count('permanent_address'))

        national_district_code = RastriyaShava.objects.values('hlcit_code').\
        annotate(total=Count('hlcit_code'))

        for item in national_district:
            if item['permanent_address']:
                national_dict[item['permanent_address']] = item['total']
        
        for item in national_district_code:
            if item['hlcit_code']:
                national_dict[item['hlcit_code']] = item['total']
        
        
        national_list.append(national_dict)

        map_api['national']=national_list

        #for federal lists
        federal_list = []
        federal_dict = {}

        federal_province = Province.objects.values('name').annotate(total=Count('pratinidhishava'))

        for item in federal_province:
            if item['name']:
                if item['name']:
                    federal_dict[item['name']] = item['total']

        federal_district = PratinidhiShava.objects.values('permanent_address').\
        annotate(total=Count('permanent_address'))

        federal_district_code = PratinidhiShava.objects.values('hlcit_code').\
        annotate(total=Count('hlcit_code'))

        for item in federal_district:
            if item['permanent_address']:
                federal_dict[item['permanent_address']] = item['total']
        
        for item in federal_district_code:
            if item['hlcit_code']:
                federal_dict[item['hlcit_code']] = item['total']

        federal_list.append(federal_dict)

        map_api['federal']=federal_list

        #for provincial lists
        provincial_list = []
        provincial_dict = {}

        provincial_province = Province.objects.values('name').annotate(total=Count('province_mahila_pratinidhi_form'))

        for item in provincial_province:
            if item['name']:
                provincial_dict[item['name']] = item['total']

        provincial_district = ProvinceMahilaPratinidhiForm.objects.values('permanent_address').\
        annotate(total=Count('permanent_address'))
        
        provincial_district_code = ProvinceMahilaPratinidhiForm.objects.values('hlcit_code').\
        annotate(total=Count('hlcit_code'))

        for item in provincial_district:
            if item['permanent_address']:
                provincial_dict[item['permanent_address']] = item['total']

        for item in provincial_district_code:
            if item['hlcit_code']:
                provincial_dict[item['hlcit_code']] = item['total']

        provincial_list.append(provincial_dict)

        map_api['provincial'] = provincial_list

        #for local lists
        # local_list = []
        # local_dict = {}

        # local_province = Province.objects.values('name').annotate(total=Count('mahilapratinidhiform'))

        # for item in local_province:
            # if item['name']:
                # local_dict[item['name']] = item['total']

        # local_district = ProvinceMahilaPratinidhiForm.objects.values('address').\
        # annotate(total=Count('address'))

        # local_district_code = ProvinceMahilaPratinidhiForm.objects.values('hlcit_code').\
        # annotate(total=Count('hlcit_code'))

        # for item in local_district:
        #     if item['address']:
        #         local_dict[item['address']] = item['total']

        # for item in local_district_code:
        #     if item['hlcit_code']:
        #         local_dict[item['hlcit_code']] = item['total_code']
        # 
        # local_list.append(local_dict)

        # map_api['local'] = local_list


        return Response(map_api)


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
                if age['age']:
                    if int(float(age['age'])) in r:
                        range_list.append(str(age_range[0]) + "-" + str(age_range[1]))

        total_arrays = np.array(np.unique(range_list, return_counts=True)).T
        age_dict = {}
        for total in total_arrays:
            age_dict['label'] = total[0]
            age_dict['total'] = total[1]
            data.append(dict(age_dict))

        total_ages['total'] = data

        #for ages per provinces
        province_age = []
        for age_range in ranges:
            age_dict = {}
            count = 0
            r = range(age_range[0], age_range[1])
            age_dict["label"] = str(age_range[0]) + "-" + str(age_range[1])
            for age in provincial_age:
                if age['age']:
                    if int(float(age['age'])) in r:
                        count = count + 1
                        age_dict[age['province_id']] = count + 1

            province_age.append(dict(age_dict))

        total_ages['provincial'] = province_age

        # for ages per party
        age_list = list(chain(provincial_age, pratinidhi_age))

        party_age = []
        for age_range in ranges:
            age_dict = {}
            count = 0
            r = range(age_range[0], age_range[1])
            age_dict["label"] = str(age_range[0]) + "-" + str(age_range[1])
            for age in age_list:
                if age['age']:
                    if int(float(age['age'])) in r:
                        count = count + 1
                        age_dict[age['party_name']] = count + 1

            party_age.append(dict(age_dict))

        total_ages['party'] = party_age


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
        national_caste = RastriyaShava.objects.all()

        castes = list(chain(pratinidhi_caste, provincial_caste, national_caste))
        totals = []
        for caste in castes:
            if caste.caste:
                totals.append(caste.caste)

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            ethnicity['label'] = total[0]
            ethnicity['total'] = total[1]

            data.append(dict(ethnicity))

        total_ethnicity['total'] = data

        #for ethnicities on basis of provinces
        province_caste = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'caste').distinct()\
        .annotate(total=Count('caste'))
        castes = []
        for provinces in province_caste:
            if provinces['caste']:
                caste = provinces['caste']
                castes.append(caste)

        caste_set = set(castes)

        province_ethinicity=[]


        for caste in caste_set:
            province_dict = {}
            province_dict['label'] = caste
            for item in province_caste:
                if caste == item['caste']:
                    if str(item['province_id']) in province_dict:
                        province_dict[str(item['province_id'])] = province_dict[str(item['province_id'])] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_ethinicity.append(dict(province_dict))


        total_ethnicity['provincial'] = province_ethinicity

        #for ethnicities on basis of political parties
        province_party_caste = ProvinceMahilaPratinidhiForm.objects.values('party_name', 'caste').distinct()\
        .annotate(total=Count('caste'))
        pratinidhi_party_caste = PratinidhiShava.objects.values('party_name', 'caste').distinct()\
        .annotate(total=Count('caste'))
        national_party_caste = RastriyaShava.objects.values('party_name', 'caste').distinct()\
        .annotate(total=Count('caste'))

        party_caste = list(chain(province_party_caste, pratinidhi_party_caste, national_party_caste))

        castes = []
        for item in party_caste:
            if item['caste']:
                caste = item['caste']
                castes.append(caste)

        caste_set = set(castes)

        party_ethinicity=[]

        for caste in caste_set:
            party_dict = {}
            party_dict['label'] = caste
            for item in party_caste:
                if caste == item['caste']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']

            party_ethinicity.append(dict(party_dict))

        total_ethnicity['party'] = party_ethinicity

        #for ethnicities on basis of nation, federal and province
        vs_ethnicity = []
        for caste in caste_set:
            vs_dict = {}
            vs_dict['label'] = caste

            for item in province_party_caste:
                if caste == item['caste']:
                    if 'province' in vs_dict:
                        vs_dict["province"] = vs_dict['province'] + item['total']
                    else:
                        vs_dict['province'] = item['total']
            
            for item in pratinidhi_party_caste:
                if caste == item['caste']:
                    if 'federal' in vs_dict:
                        vs_dict["federal"] = vs_dict['federal'] + item['total']
                    else:
                        vs_dict['federal'] = item['total']

            for item in national_party_caste:
                if caste == item['caste']:
                    if 'national' in vs_dict:
                        vs_dict["national"] = vs_dict['national'] + item['total']
                    else:
                        vs_dict['national'] = item['total']
            
            vs_ethnicity.append(dict(vs_dict))
                    
        total_ethnicity['nationalvsfederalvsprovincial'] = vs_ethnicity

        return Response(total_ethnicity)


class MotherTongueViewSet(views.APIView):

    def get(self, request):

        total_mother_tongue = {}
        data = []
        mother_tongue={}

        #for total mother_tongues
        pratinidhi_lang = PratinidhiShava.objects.all()
        provincial_lang = ProvinceMahilaPratinidhiForm.objects.all()
        national_lang = RastriyaShava.objects.all()

        languages = list(chain(pratinidhi_lang, provincial_lang, national_lang))
        totals = []
        for language in languages:
            if language.mother_tongue:
                totals.append(language.mother_tongue)

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            mother_tongue['label'] = total[0]
            mother_tongue['total'] = total[1]

            data.append(dict(mother_tongue))

        total_mother_tongue['total'] = data

        #for mother_tongue on basis of provinces
        province_mother_tongue = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'mother_tongue')\
        .distinct().annotate(total=Count('mother_tongue'))
        languages = []
        
        for language in province_mother_tongue:
            if language['mother_tongue']:
                lang = language['mother_tongue']
                languages.append(lang)

        language_set = set(languages)

        province_language=[]


        for language in language_set:
            province_dict = {}
            province_dict['label'] = language
            for item in province_mother_tongue:
                if language == item['mother_tongue']:
                    if str(item['province_id']) in province_dict:
                        province_dict[str(item['province_id'])] = province_dict[str(item['province_id'])] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_language.append(dict(province_dict))


        total_mother_tongue['provincial'] = province_language

        #for mother tongue on basis of political parties
        province_party_lang = ProvinceMahilaPratinidhiForm.objects.values('party_name', 'mother_tongue')\
        .distinct().annotate(total=Count('mother_tongue'))
        pratinidhi_party_lang = PratinidhiShava.objects.values('party_name', 'mother_tongue')\
        .distinct().annotate(total=Count('mother_tongue'))
        national_party_lang = RastriyaShava.objects.values('party_name', 'mother_tongue')\
        .distinct().annotate(total=Count('mother_tongue'))

        party_lang = list(chain(province_party_lang, pratinidhi_party_lang, national_party_lang))

        languages = []
        for item in party_lang:
            if item['mother_tongue']:
                lang = item['mother_tongue']
                languages.append(lang)

        language_set = set(languages)

        party_language=[]

        for language in language_set:
            party_dict = {}
            party_dict['label'] = language
            for item in party_lang:
                if language == item['mother_tongue']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']

            party_language.append(dict(party_dict))

        total_mother_tongue['party'] = party_language

        #for mother tongue on basis of nation, federal and province
        vs_language = []
        for language in language_set:
            vs_dict = {}
            vs_dict['label'] = language

            for item in province_party_lang:
                if language == item['mother_tongue']:
                    if "province" in vs_dict:
                        vs_dict['province'] = vs_dict['province'] + item['total']
                    else:
                        vs_dict["province"] = item['total']
            

            for item in pratinidhi_party_lang:
                if language == item['mother_tongue']:
                    if "federal" in vs_dict:
                        vs_dict['federal'] = vs_dict['federal'] + item['total']
                    else:
                        vs_dict["federal"] = item['total']

            for item in national_party_lang:
                if language == item['mother_tongue']:
                    if "national" in vs_dict:
                        vs_dict['national'] = vs_dict['national'] + item['total']
                    else:
                        vs_dict["national"] = item['total']
            
            vs_language.append(dict(vs_dict))
                    
        total_mother_tongue['nationalvsfederalvsprovincial'] = vs_language


        return Response(total_mother_tongue)


class EducationViewSet(views.APIView):

   def get(self, request):

        total_education = {}
        data = []
        edu={}

        #for total educational qualification
        pratinidhi_education = PratinidhiShava.objects.all()
        provincial_education = ProvinceMahilaPratinidhiForm.objects.all()
        national_education = RastriyaShava.objects.all()

        educations = list(chain(pratinidhi_education, provincial_education, national_education))
        totals = []
        for education in educations:
            if education.educational_qualification:
                totals.append(education.educational_qualification)

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            edu['label'] = total[0]
            edu['total'] = total[1]

            data.append(dict(edu))

        total_education['total'] = data

        #for educational qualification on basis of provinces
        province_education = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'educational_qualification')\
        .distinct().annotate(total=Count('educational_qualification'))
        educations = []

        for education in province_education:
            if education['educational_qualification']:
                edu = education['educational_qualification']
                educations.append(edu)

        education_set = set(educations)

        province_edu=[]


        for education in education_set:
            province_dict = {}
            province_dict['label'] = education
            for item in province_education:
                if education == item['educational_qualification']:
                    if str(item['province_id']) in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_edu.append(dict(province_dict))


        total_education['provincial'] = province_edu

        #for ethnicities on basis of political parties
        province_party_edu = ProvinceMahilaPratinidhiForm.objects.values('party_name', 'educational_qualification')\
        .distinct().annotate(total=Count('educational_qualification'))
        pratinidhi_party_edu = PratinidhiShava.objects.values('party_name', 'educational_qualification')\
        .distinct().annotate(total=Count('educational_qualification'))
        national_party_edu = RastriyaShava.objects.values('party_name', 'educational_qualification')\
        .distinct().annotate(total=Count('educational_qualification'))

        party_edu = list(chain(province_party_edu, pratinidhi_party_edu, national_party_edu))

        educations = []
        for item in party_edu:
            if item['educational_qualification']:
                edu = item['educational_qualification']
                educations.append(edu)
        
        education_set = set(educations)

        party_education=[]

        for education in education_set:
            party_dict = {}
            party_dict['label'] = education
            for item in party_edu:
                if item['educational_qualification'] is not None:
                    if education == item['educational_qualification']:
                        if item['party_name'] in party_dict:
                            party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                        else:
                            party_dict[item['party_name']] = item['total']

            party_education.append(dict(party_dict))

        total_education['party'] = party_education

        #for education on basis of nation, federal and province
        vs_education = []
        for education in education_set:
            vs_dict = {}
            vs_dict['label'] = education

            for item in province_party_edu:
                if education == item['educational_qualification']:
                    if "province" in vs_dict:
                        vs_dict['province'] = vs_dict['province'] + item['total']
                    else:
                        vs_dict["province"] = item['total']
            

            for item in pratinidhi_party_edu:
                if education == item['educational_qualification']:
                    if "federal" in vs_dict:
                        vs_dict['federal'] = vs_dict['federal'] + item['total']
                    else:
                        vs_dict["federal"] = item['total']

            for item in national_party_edu:
                if item['educational_qualification']:
                    if education == item['educational_qualification']:
                        if "national" in vs_dict:
                            vs_dict['national'] = vs_dict['national'] + item['total']
                        else:
                            vs_dict["national"] = item['total']
            
            vs_education.append(dict(vs_dict))
                    
        total_education['nationalvsfederalvsprovincial'] = vs_education

        
        return Response(total_education)


class ElectionTypeViewSet(views.APIView):

    def get(self, request):

        total_election_type = {}
        data = []
        election_type={}

        #for total election type
        pratinidhi = PratinidhiShava.objects.all()
        provincial = ProvinceMahilaPratinidhiForm.objects.all()
        national = RastriyaShava.objects.all()

        election_types = list(chain(pratinidhi, provincial, national))
        totals = []
        for election in election_types:
            if election.nirwachit_prakriya:
                totals.append(election.nirwachit_prakriya.title().strip(" "))

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            election_type['label'] = total[0]
            election_type['total'] = total[1]

            data.append(dict(election_type))

        total_election_type['total'] = data

        #for election type on basis of provinces
        province_election = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'nirwachit_prakriya')\
        .distinct().annotate(total=Count('nirwachit_prakriya'))
        election_types = []
        for election in province_election:
            if election['nirwachit_prakriya']:
                elec = election['nirwachit_prakriya'].title().strip(" ")
                election_types.append(elec)

        election_set = set(election_types)

        province_elect=[]


        for elect in election_set:
            province_dict = {}
            province_dict['label'] = elect
            for item in province_election:
                if elect in item['nirwachit_prakriya']:
                    if str(item['province_id']) in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_elect.append(dict(province_dict))


        total_election_type['provincial'] = province_elect

        #for election type on basis of political parties
        province_party_election = ProvinceMahilaPratinidhiForm.objects.values('party_name', 'nirwachit_prakriya')\
        .distinct().annotate(total=Count('nirwachit_prakriya'))
        pratinidhi_party_election = PratinidhiShava.objects.values('party_name', 'nirwachit_prakriya')\
        .distinct().annotate(total=Count('nirwachit_prakriya'))
        national_party_election = RastriyaShava.objects.values('party_name', 'nirwachit_prakriya')\
        .distinct().annotate(total=Count('nirwachit_prakriya'))

        party_election = list(chain(province_party_election, pratinidhi_party_election, national_party_election))

        elections = []
        for item in party_election:
            if item['nirwachit_prakriya']:
                elect = item['nirwachit_prakriya'].title().strip(" ")
                elections.append(elect)

        election_set = set(elections)

        party_elections=[]

        for elect in election_set:
            party_dict = {}
            party_dict['label'] = elect
            for item in party_election:
                if elect in item['nirwachit_prakriya']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']

            party_elections.append(dict(party_dict))

        total_election_type['party'] = party_elections


        #for election type on basis of nation, federal and province
        vs_election = []
        for election in election_set:
            vs_dict = {}
            vs_dict['label'] = election

            for item in province_party_election:
                if election == item['nirwachit_prakriya']:
                    if "province" in vs_dict:
                        vs_dict['province'] = vs_dict['province'] + item['total']
                    else:
                        vs_dict["province"] = item['total']
            

            for item in pratinidhi_party_election:
                if election == item['nirwachit_prakriya']:
                    if "federal" in vs_dict:
                        vs_dict['federal'] = vs_dict['federal'] + item['total']
                    else:
                        vs_dict["federal"] = item['total']

            for item in national_party_election:
                if election == item['nirwachit_prakriya']:
                    if "national" in vs_dict:
                        vs_dict['national'] = vs_dict['national'] + item['total']
                    else:
                        vs_dict["national"] = item['total']
            
            vs_election.append(dict(vs_dict))
                    
        total_election_type['nationalvsfederalvsprovincial'] = vs_election

        return Response(total_election_type)


class PoliticalEngagementViewSet(views.APIView):

    def get(self, request):

        total_years = {}
        data = []
        ranges = []
        rastriya_political_year = RastriyaShava.objects.values('party_joined_date', 'province_id', 'party_name')
        pratinidhi_political_year = PratinidhiShava.objects.values('party_joined_date', 'province_id', 'party_name')
        provincial_political_year = ProvinceMahilaPratinidhiForm.objects.values('party_joined_date', 'province_id', 'party_name')
        # local_age = MahilaPratinidhiForm.objects.values('age')

        # for total years 
        years = list(chain(rastriya_political_year, pratinidhi_political_year, provincial_political_year))

        lists = 1
        while lists < 70:
            sub_ranges = []
            sub_lists = lists
            sub_ranges.append(sub_lists)
            while sub_lists <= lists:
                sub_lists = sub_lists + 5
                sub_ranges.append(sub_lists)
            ranges.append(sub_ranges)
            lists = lists + 5


        range_list = []

        for year_range in ranges:
            r = range(year_range[0], year_range[1])
            for age in years:
                if age['party_joined_date']:
                    if (2075 - int(float(age['party_joined_date']))) in r:
                        range_list.append(str(year_range[0]) + "-" + str(year_range[1]))

        total_arrays = np.array(np.unique(range_list, return_counts=True)).T
        year_dict = {}
        for total in total_arrays:
            year_dict['label'] = total[0]
            year_dict['total'] = total[1]
            data.append(dict(year_dict))

        total_years['total'] = data

        #for years per provinces
        province_year = []
        for year_range in ranges:
            age_dict = {}
            count = 0
            r = range(year_range[0], year_range[1])
            age_dict["label"] = str(year_range[0]) + "-" + str(year_range[1])
            for year in provincial_political_year:
                if year['party_joined_date']:
                    if (2071 - int(float(year['party_joined_date']))) in r:
                        count = count + 1
                        age_dict[year['province_id']] = count + 1

            province_year.append(dict(age_dict))

        total_years['provincial'] = province_year

        # for years per party
        party_year = []
        for year_range in ranges:
            age_dict = {}
            count = 0
            r = range(year_range[0], year_range[1])
            age_dict["label"] = str(year_range[0]) + "-" + str(year_range[1])
            for age in years:
                if age['party_joined_date']:
                    if(2075 - int(float(age['party_joined_date']))) in r:
                        count = count + 1
                        age_dict[age['party_name']] = count + 1

            party_year.append(dict(age_dict))

        total_years['party'] = party_year

        #for years of national vs province vs federal
        


        return Response(total_years)



class MaritalStatusViewSet(views.APIView):

    def get(self, request):

        total_maritalstatus_dict = {}
        data_list = []
        maritalstatus_dict = {}

        #for marital status qualification
        pratinidhi = PratinidhiShava.objects.all()
        provincial = ProvinceMahilaPratinidhiForm.objects.all()
        national = RastriyaShava.objects.all()

        maritalstatus_list = list(chain(pratinidhi, provincial, national))
        totals = []
        for marital in maritalstatus_list:
            if marital.marital_status:
                totals.append(marital.marital_status)

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            maritalstatus_dict['label'] = total[0]
            maritalstatus_dict['total'] = total[1]

            data_list.append(dict(maritalstatus_dict))

        total_maritalstatus_dict['total'] = data_list

        #for marital status on basis of provinces
        province_maritalstatus = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'marital_status')\
        .distinct().annotate(total=Count('marital_status'))
        marital_status_list = []
        for marital in province_maritalstatus:
            if marital['marital_status']:
                maritals = marital['marital_status']
                marital_status_list.append(maritals)

        marital_status_set = set(marital_status_list)

        province_marital_list = []


        for marital in marital_status_set:
            province_dict = {}
            province_dict['label'] = marital
            for item in province_maritalstatus:
                if marital == item['marital_status']:
                    if str(item['province_id']) in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_marital_list.append(dict(province_dict))


        total_maritalstatus_dict['provincial'] = province_marital_list

        #for marital status on basis of political parties
        province_party_marital = ProvinceMahilaPratinidhiForm.objects.values('party_name', 'marital_status')\
        .distinct().annotate(total=Count('marital_status'))
        pratinidhi_party_marital = PratinidhiShava.objects.values('party_name', 'marital_status')\
        .distinct().annotate(total=Count('marital_status'))
        national_party_marital = RastriyaShava.objects.values('party_name', 'marital_status')\
        .distinct().annotate(total=Count('marital_status'))

        party_marital =  list(chain(province_party_marital, pratinidhi_party_marital, national_party_marital))

        marital_list = []
        for item in party_marital:
            if item['marital_status']:
                marital = item['marital_status']
                marital_list.append(marital)

        marital_set = set(marital_list)

        party_marital_list = []

        for m in marital_set:
            party_dict = {}
            party_dict['label'] = m
            for item in party_marital:
                if m == item['marital_status']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']

            party_marital_list.append(dict(party_dict))

        total_maritalstatus_dict['party'] = party_marital_list


        #for election type on basis of nation, federal and province
        vs_marital = []
        for marital in marital_set:
            vs_dict = {}
            vs_dict['label'] = marital

            for item in province_party_marital:
                if marital == item['marital_status']:
                    if "province" in vs_dict:
                        vs_dict['province'] = vs_dict['province'] + item['total']
                    else:
                        vs_dict["province"] = item['total']

            for item in pratinidhi_party_marital:
                if marital == item['marital_status']:
                    if "federal" in vs_dict:
                        vs_dict['federal'] = vs_dict['federal'] + item['total']
                    else:
                        vs_dict["federal"] = item['total']

            for item in national_party_marital:
                if marital == item['marital_status']:
                    if "national" in vs_dict:
                        vs_dict['national'] = vs_dict['national'] + item['total']
                    else:
                        vs_dict["national"] = item['total']

            vs_marital.append(dict(vs_dict))
                    
        total_maritalstatus_dict['nationalvsfederalvsprovincial'] = vs_marital

        return Response(total_maritalstatus_dict)


class ElectionParticipate(views.APIView):

    def get(self, request):
        total_election_before_dict = {}
        data_list = []
        election_before_dict = {}

        #for total educational qualification
        pratinidhi = PratinidhiShava.objects.all()
        provincial = ProvinceMahilaPratinidhiForm.objects.all()
        national = RastriyaShava.objects.all()

        election_before_list = list(chain(pratinidhi, provincial, national))
        totals = []
        for elect in election_before_list:
            if elect.aaja_vanda_agadi_chunab_ladnu_vayeko_chha:
                totals.append(elect.aaja_vanda_agadi_chunab_ladnu_vayeko_chha)

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            election_before_dict['label'] = total[0]
            election_before_dict['total'] = total[1]

            data_list.append(dict(election_before_dict))

        total_election_before_dict['total'] = data_list

        #for election experience on basis of provinces
        province_election_before = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'aaja_vanda_agadi_chunab_ladnu_vayeko_chha')\
        .distinct().annotate(total=Count('aaja_vanda_agadi_chunab_ladnu_vayeko_chha'))
        election_before_list = []
        for election_before in province_election_before:
            if election_before['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                elections = election_before['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']
                election_before_list.append(elections)

        election_before_set = set(election_before_list)

        province_election_before_list = []


        for election in election_before_set:
            province_dict = {}
            province_dict['label'] = election
            for item in province_election_before:
                if election in item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                    if str(item['province_id']) in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_election_before_list.append(dict(province_dict))


        total_election_before_dict['provincial'] = province_election_before_list

        #for election experience on basis of political parties
        province_party_election_before = ProvinceMahilaPratinidhiForm.objects\
        .values('party_name', 'aaja_vanda_agadi_chunab_ladnu_vayeko_chha')\
        .distinct().annotate(total=Count('aaja_vanda_agadi_chunab_ladnu_vayeko_chha'))
        pratinidhi_party_election_before = PratinidhiShava.objects\
        .values('party_name', 'aaja_vanda_agadi_chunab_ladnu_vayeko_chha')\
        .distinct().annotate(total=Count('aaja_vanda_agadi_chunab_ladnu_vayeko_chha'))
        national_party_election_before = RastriyaShava.objects\
        .values('party_name', 'aaja_vanda_agadi_chunab_ladnu_vayeko_chha')\
        .distinct().annotate(total=Count('aaja_vanda_agadi_chunab_ladnu_vayeko_chha'))

        party_election_before_list =  list(
            chain(
                province_party_election_before, pratinidhi_party_election_before, national_party_election_before))

        election_before_list = []
        for item in party_election_before_list:
            if item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                election_before = item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']
                election_before_list.append(election_before)

        election_before_set = set(election_before_list)

        party_election_before = []

        for m in election_before_set:
            party_dict = {}
            party_dict['label'] = m
            for item in party_election_before_list:
                if item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                    if m in item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                        if item['party_name'] in party_dict:
                            party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                        else:
                            party_dict[item['party_name']] = item['total']

            party_election_before.append(dict(party_dict))

        total_election_before_dict['party'] = party_election_before
        
        #for election experience on basis of nation, federal and province
        vs_election_before = []
        for elections in election_before_set:
            vs_dict = {}
            vs_dict['label'] = elections

            for item in province_party_election_before:
                if item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                    if elections == item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                        if "province" in vs_dict:
                            vs_dict['province'] = vs_dict['province'] + item['total']
                        else:
                            vs_dict["province"] = item['total']

            for item in pratinidhi_party_election_before:
                if item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                    if elections == item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                        if "federal" in vs_dict:
                            vs_dict['federal'] = vs_dict['federal'] + item['total']
                        else:
                            vs_dict["federal"] = item['total']
            
            for item in national_party_election_before:
                if item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                    if elections == item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                        if 'national' in vs_dict:
                            vs_dict['national'] = vs_dict['national'] + item['total']
                        else:
                            vs_dict['national'] = item['total']

            vs_election_before.append(dict(vs_dict))
                    
        total_election_before_dict['nationalvsfederalvsprovincial'] = vs_election_before

        return Response(total_election_before_dict)


class PartyViewSet(views.APIView):

    def get(self, request):

        total_party_dict = {}
        data_list = []
        party_dict = {}

        #for total educational qualification
        pratinidhi = PratinidhiShava.objects.all()
        provincial = ProvinceMahilaPratinidhiForm.objects.all()
        national = RastriyaShava.objects.all()

        party_list = list(chain(pratinidhi, provincial, national))
        totals = []
        for party in party_list:
            if party.party_name:
                totals.append(party.party_name)

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            party_dict['label'] = total[0]
            party_dict['total'] = total[1]

            data_list.append(dict(party_dict))

        total_party_dict['total'] = data_list
        
        #for parties on basis of provinces
        province_party = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'party_name')\
        .distinct().annotate(total=Count('party_name'))
        party_list = []
        for party in province_party:
            if party['party_name']:
                parties = party['party_name']
                party_list.append(parties)

        party_set = set(party_list)

        province_party_list = []


        for party in party_set:
            province_dict = {}
            province_dict['label'] = party
            for item in province_party:
                if party in item['party_name']:
                    if str(item['province_id']) in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_party_list.append(dict(province_dict))


        total_party_dict['provincial'] = province_party_list

        #for parties on basis of nation, federal and province
        province_party = ProvinceMahilaPratinidhiForm.objects\
        .values('party_name')\
        .distinct().annotate(total=Count('party_name'))
        pratinidhi_party = PratinidhiShava.objects\
        .values('party_name')\
        .distinct().annotate(total=Count('party_name'))
        national_party = RastriyaShava.objects\
        .values('party_name')\
        .distinct().annotate(total=Count('party_name'))


        vs_party = []
        for party in party_set:
            vs_dict = {}
            vs_dict['label'] = party

            for item in province_party:
                if item['party_name']:
                    if party == item['party_name']:
                        if "province" in vs_dict:
                            vs_dict['province'] = vs_dict['province'] + item['total']
                        else:
                            vs_dict["province"] = item['total']

            for item in pratinidhi_party:
                if item['party_name']:
                    if party == item['party_name']:
                        if "federal" in vs_dict:
                            vs_dict['federal'] = vs_dict['federal'] + item['total']
                        else:
                            vs_dict["federal"] = item['total']
            
            for item in national_party:
                if item['party_name']:
                    if party == item['party_name']:
                        if 'national' in vs_dict:
                            vs_dict['national'] = vs_dict['national'] + item['total']
                        else:
                            vs_dict['national'] = item['total']

            vs_party.append(dict(vs_dict))
                    
        total_party_dict['nationalvsfederalvsprovincial'] = vs_party

        return Response(total_party_dict)


class CommitmentViewSet(views.APIView):

    def get(self, request):
        
        commitment_dict = {}
        data_list = []
        total_commitment_dict = {}

        #for total political commitment

        #fetch each commitments for national, pratinidhi and provincial
        province_political_commitment = ProvinceMahilaPratinidhiForm.objects.values(
            'party_name', 'nirwachit_chetra_pratiko_pratibadhata', 'province_id'
            )
        national_political_commitment = RastriyaShava.objects.values(
            'party_name', 'nirwachit_chetra_pratiko_pratibadhata'
            )        
        federal_political_commitment = PratinidhiShava.objects.values(
            'party_name', 'nirwachit_chetra_pratiko_pratibadhata'
            ) 
        commitment_lists = list(chain(national_political_commitment, federal_political_commitment, province_political_commitment))
        commitment_set = ()
        commitments_list = []
        

        for commitment in commitment_lists:
            for item in commitment['nirwachit_chetra_pratiko_pratibadhata'].split(","):
                if item:
                    item = item.strip(" ")
                    commitments_list.append(item.title())

        commitment_set = set(commitments_list)
        
        totals = []

        for item in commitments_list:
            if item in commitment_set:
                totals.append(item)
        
        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            commitment_dict['label'] = total[0]
            commitment_dict['total'] = total[1]

            data_list.append(dict(commitment_dict))

        total_commitment_dict['total'] = data_list

        #for political commitment on basis of province
        province_political_commitment_list = []

        for commitment in commitment_set:
            province_dict = {}
            province_dict['label'] = commitment
            for item in province_political_commitment:
                for i in item['nirwachit_chetra_pratiko_pratibadhata'].split(","):
                    if i.title().strip(" ") in commitment:
                        if str(item['province_id']) in province_dict:
                            province_dict[str(item['province_id'])] = province_dict[str(item['province_id'])] + 1
                        else:
                            province_dict[str(item['province_id'])] = 1
            
            province_political_commitment_list.append(dict(province_dict))

        total_commitment_dict['provincial'] = province_political_commitment_list

        #for political commitments on basis of party
        list_commitment = list(chain(province_political_commitment, national_political_commitment, federal_political_commitment))
        party_political_commitment_list = []

        for commitment in commitment_set:
            party_dict = {}
            party_dict['label'] = commitment
            for item in list_commitment:
                for i in item['nirwachit_chetra_pratiko_pratibadhata'].split(","):
                    if i.title().strip(" ") in commitment:
                        if item['party_name']:
                            if item['party_name'] in party_dict:
                                party_dict[item['party_name']] = party_dict[item['party_name']] + 1
                            else:
                                party_dict[item['party_name']] = 1
            
            party_political_commitment_list.append(dict(party_dict))

        total_commitment_dict['party'] = party_political_commitment_list


        return Response(total_commitment_dict)


class DistrictsViewSet(ReadOnlyModelViewSet):
    serializer_class = DistrictsSerializer

    def get_queryset(self):
        queryset = District.objects.all().select_related('province')
        province_query = self.request.query_params.get('province_id', None)
        if province_query is not None:
            queryset = queryset.filter(province=province_query)
        return queryset

class HlcitViewSet(ReadOnlyModelViewSet):
    serializer_class = HlcitSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = chain(
            RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit']),
            PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit']),
            ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit'])
        )
            
        return queryset
