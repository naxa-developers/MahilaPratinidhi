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
def districts_geojson(request):

    data = {}
    try:
        with open('jsons/district.geojson') as f:
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
    print(district)

    data = {}
    try:
        with open('jsons/gapanapa/{}.geojson'.format(district.capitalize())) as f:
            print(f)
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

        total_age_list = []
        for age in ages:
            if age['age']:
                total_age_list.append(int(float(age['age'])))

        total_ages['all'] = total_age_list

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
            for age in ages:
                if age['age']:
                    if int(float(age['age'])) in r:
                        count = count + 1
                        age_dict[age['province_id']] = count + 1

            province_age.append(dict(age_dict))

        total_ages['provincial'] = province_age

        # for ages per party

        party_age = []
        for age_range in ranges:
            age_dict = {}
            count = 0
            r = range(age_range[0], age_range[1])
            age_dict["label"] = str(age_range[0]) + "-" + str(age_range[1])
            for age in ages:
                if age['age']:
                    if int(float(age['age'])) in r:
                        count = count + 1
                        age_dict[age['party_name']] = count + 1

            party_age.append(dict(age_dict))

        total_ages['party'] = party_age

        #for age range on basis of national, federal and province
        vs = []
        for age_range in ranges:
            vs_dict = {}
            vs_list = []
            r = range(age_range[0], age_range[1])
            vs_dict["label"] = str(age_range[0]) + "-" + str(age_range[1])

            for item in rastriya_age:
                if item['age']:
                    if int(float(item['age'])) in r:
                        vs_list.append('national')

            for item in pratinidhi_age:
                if item['age']:
                    if int(float(item['age'])) in r:
                        vs_list.append('federal')

            for item in provincial_age:
                if item['age']:
                    if int(float(item['age'])) in r:
                        vs_list.append('province')

            total_arrays = np.array(np.unique(vs_list, return_counts=True)).T

            for total in total_arrays:
                vs_dict[total[0]] = total[1]

            vs.append(dict(vs_dict))

        total_ages['nationalvsfederalvsprovincial'] = vs

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
        provincial_caste = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'party_name', 'caste').distinct()\
        .annotate(total=Count('caste'))
        national_caste = RastriyaShava.objects.values('province_id', 'party_name', 'caste').distinct()\
        .annotate(total=Count('caste'))
        pratinidhi_caste = PratinidhiShava.objects.values('province_id', 'party_name', 'caste').distinct()\
        .annotate(total=Count('caste'))
        # local_caste = MahilaPratinidhiForm.objects.values('province_id', 'caste').distinct()\
        # .annotate(total=Count('caste'))
        
        prv_castes = list(chain(pratinidhi_caste, provincial_caste, national_caste))

        castes = []
        for provinces in prv_castes:
            if provinces['caste']:
                caste = provinces['caste']
                castes.append(caste)

        caste_set = set(castes)

        province_ethinicity=[]

        for caste in caste_set:
            province_dict = {}
            province_dict['label'] = caste
            for item in prv_castes:
                if caste == item['caste']:
                    if item['province_id'] in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
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
        local_party_caste = MahilaPratinidhiForm.objects.values('party_name', 'caste').distinct()\
        .annotate(total=Count('caste'))

        party_caste = list(chain(province_party_caste, pratinidhi_party_caste, national_party_caste, local_party_caste))

        castes = []
        for item in prv_castes:
            if item['caste']:
                caste = item['caste']
                castes.append(caste)

        caste_set = set(castes)

        party_ethinicity=[]

        for caste in caste_set:
            party_dict = {}
            party_dict['label'] = caste
            for item in prv_castes:
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

            for item in provincial_caste:
                if caste == item['caste']:
                    if 'province' in vs_dict:
                        vs_dict["province"] = vs_dict['province'] + item['total']
                    else:
                        vs_dict['province'] = item['total']

            for item in pratinidhi_caste:
                if caste == item['caste']:
                    if 'federal' in vs_dict:
                        vs_dict["federal"] = vs_dict['federal'] + item['total']
                    else:
                        vs_dict['federal'] = item['total']

            for item in national_caste:
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
        province_mother_tongue = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'party_name', 'mother_tongue')\
        .distinct().annotate(total=Count('mother_tongue'))
        national_mother_tongue = RastriyaShava.objects.values('province_id', 'party_name', 'mother_tongue')\
        .distinct().annotate(total=Count('mother_tongue'))
        pratinidhi_mother_tongue = PratinidhiShava.objects.values('province_id', 'party_name', 'mother_tongue')\
        .distinct().annotate(total=Count('mother_tongue'))
        # local_mother_tongue = MahilaPratinidhiForm.objects.values('province_id', 'party_name', 'mother_tongue')\
        # .distinct().annotate(total=Count('mother_tongue'))

        province_mother_tongues = list(chain(province_mother_tongue, national_mother_tongue, pratinidhi_mother_tongue))
        languages = []
        
        for language in province_mother_tongues:
            if language['mother_tongue']:
                lang = language['mother_tongue']
                languages.append(lang)

        language_set = set(languages)

        province_language=[]


        for language in language_set:
            province_dict = {}
            province_dict['label'] = language
            for item in province_mother_tongues:
                if language == item['mother_tongue']:
                    if item['province_id'] in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_language.append(dict(province_dict))


        total_mother_tongue['provincial'] = province_language

        #for mother tongue on basis of political parties
        languages = []
        for item in province_mother_tongues:
            if item['mother_tongue']:
                lang = item['mother_tongue']
                languages.append(lang)

        language_set = set(languages)

        party_language=[]

        for language in language_set:
            party_dict = {}
            party_dict['label'] = language
            for item in province_mother_tongues:
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

            for item in province_mother_tongue:
                if language == item['mother_tongue']:
                    if "province" in vs_dict:
                        vs_dict['province'] = vs_dict['province'] + item['total']
                    else:
                        vs_dict["province"] = item['total']


            for item in pratinidhi_mother_tongue:
                if language == item['mother_tongue']:
                    if "federal" in vs_dict:
                        vs_dict['federal'] = vs_dict['federal'] + item['total']
                    else:
                        vs_dict["federal"] = item['total']

            for item in national_mother_tongue:
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
        province_education = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'party_name', 'educational_qualification')\
        .distinct().annotate(total=Count('educational_qualification'))
        national_education = RastriyaShava.objects.values('province_id', 'party_name', 'educational_qualification')\
        .distinct().annotate(total=Count('educational_qualification'))
        pratinidhi_education = PratinidhiShava.objects.values('province_id', 'party_name', 'educational_qualification')\
        .distinct().annotate(total=Count('educational_qualification'))
        # local_education = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'party_name', 'educational_qualification')\
        # .distinct().annotate(total=Count('educational_qualification'))
        
        province_educations = list(chain(province_education, national_education, pratinidhi_education))

        educations = []

        for education in province_educations:
            if education['educational_qualification']:
                edu = education['educational_qualification']
                educations.append(edu)

        education_set = set(educations)

        province_edu=[]


        for education in education_set:
            province_dict = {}
            province_dict['label'] = education
            for item in province_educations:
                if education == item['educational_qualification']:
                    if item['province_id'] in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_edu.append(dict(province_dict))


        total_education['provincial'] = province_edu

        #for ethnicities on basis of political parties
        educations = []
        for item in province_educations:
            if item['educational_qualification']:
                edu = item['educational_qualification']
                educations.append(edu)

        education_set = set(educations)

        party_education=[]

        for education in education_set:
            party_dict = {}
            party_dict['label'] = education
            for item in province_educations:
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

            for item in province_education:
                if education == item['educational_qualification']:
                    if "province" in vs_dict:
                        vs_dict['province'] = vs_dict['province'] + item['total']
                    else:
                        vs_dict["province"] = item['total']


            for item in pratinidhi_education:
                if education == item['educational_qualification']:
                    if "federal" in vs_dict:
                        vs_dict['federal'] = vs_dict['federal'] + item['total']
                    else:
                        vs_dict["federal"] = item['total']

            for item in national_education:
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
        province_election = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'party_name', 'nirwachit_prakriya')\
        .distinct().annotate(total=Count('nirwachit_prakriya'))
        national_election = RastriyaShava.objects.values('province_id', 'party_name', 'nirwachit_prakriya')\
        .distinct().annotate(total=Count('nirwachit_prakriya'))
        pratinidhi_election = PratinidhiShava.objects.values('province_id', 'party_name', 'nirwachit_prakriya')\
        .distinct().annotate(total=Count('nirwachit_prakriya'))
        
        election_list = list(chain(province_election, national_election, pratinidhi_election)) 

        election_types = []
        for election in election_list:
            if election['nirwachit_prakriya']:
                elec = election['nirwachit_prakriya'].title().strip(" ")
                election_types.append(elec)

        election_set = set(election_types)

        province_elect=[]
        for elect in election_set:
            province_dict = {}
            province_dict['label'] = elect
            for item in election_list:
                if elect == item['nirwachit_prakriya'].title().strip(" "):
                    if item['province_id'] in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_elect.append(dict(province_dict))


        total_election_type['provincial'] = province_elect

        #for election type on basis of political parties
        elections = []
        for item in election_list:
            if item['nirwachit_prakriya']:
                elect = item['nirwachit_prakriya'].title().strip(" ")
                elections.append(elect)

        election_set = set(elections)

        party_elections=[]

        for elect in election_set:
            party_dict = {}
            party_dict['label'] = elect
            for item in election_list:
                if elect == item['nirwachit_prakriya'].title().strip(" "):
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

            for item in province_election:
                if election == item['nirwachit_prakriya'].title().strip(" "):
                    if "province" in vs_dict:
                        vs_dict['province'] = vs_dict['province'] + item['total']
                    else:
                        vs_dict["province"] = item['total']


            for item in pratinidhi_election:
                if election == item['nirwachit_prakriya'].title().strip(" "):
                    if "federal" in vs_dict:
                        vs_dict['federal'] = vs_dict['federal'] + item['total']
                    else:
                        vs_dict["federal"] = item['total']

            for item in national_election:
                if election == item['nirwachit_prakriya'].title().strip(" "):
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
        years = list(chain(rastriya_political_year, pratinidhi_political_year, provincial_political_year, local_political_year))

        total_year_list = []

        for year in years:
            if year['party_joined_date']:
                total_year_list.append(2075 - int(float(year['party_joined_date'])))

        total_years['all'] = total_year_list

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
            for year in years:
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

        #for political engagement on basis of national, federal and province
        vs = []
        for year_range in ranges:
            vs_dict = {}
            vs_list = []
            r = range(year_range[0], year_range[1])
            vs_dict["label"] = str(year_range[0]) + "-" + str(year_range[1])

            for item in rastriya_political_year:
                if item['party_joined_date']:
                    if(2075 - int(float(item['party_joined_date']))) in r:
                        vs_list.append('national')

            for item in pratinidhi_political_year:
                if item['party_joined_date']:
                    if(2075 - int(float(item['party_joined_date']))) in r:
                        vs_list.append('federal')

            for item in provincial_political_year:
                if item['party_joined_date']:
                    if(2075 - int(float(item['party_joined_date']))) in r:
                        vs_list.append('province')

            total_arrays = np.array(np.unique(vs_list, return_counts=True)).T

            for total in total_arrays:
                vs_dict[total[0]] = total[1]

            vs.append(dict(vs_dict))

        total_years['nationalvsfederalvsprovincial'] = vs

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
        province_maritalstatus = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'party_name', 'marital_status')\
        .distinct().annotate(total=Count('marital_status'))
        national_maritalstatus = RastriyaShava.objects.values('province_id', 'party_name', 'marital_status')\
        .distinct().annotate(total=Count('marital_status'))
        pratinidhi_maritalstatus = PratinidhiShava.objects.values('province_id', 'party_name', 'marital_status')\
        .distinct().annotate(total=Count('marital_status'))

        province_marital = list(chain(province_maritalstatus, national_maritalstatus, pratinidhi_maritalstatus))

        marital_status_list = []
        for marital in province_marital:
            if marital['marital_status']:
                maritals = marital['marital_status']
                marital_status_list.append(maritals)

        marital_status_set = set(marital_status_list)

        province_marital_list = []


        for marital in marital_status_set:
            province_dict = {}
            province_dict['label'] = marital
            for item in province_marital:
                if marital == item['marital_status']:
                    if item['province_id'] in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_marital_list.append(dict(province_dict))


        total_maritalstatus_dict['provincial'] = province_marital_list

        #for marital status on basis of political parties
        party_marital_list = []

        for m in marital_status_set:
            party_dict = {}
            party_dict['label'] = m
            for item in province_marital:
                if m == item['marital_status']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']

            party_marital_list.append(dict(party_dict))

        total_maritalstatus_dict['party'] = party_marital_list


        #for election type on basis of nation, federal and province
        vs_marital = []
        for marital in marital_status_set:
            vs_dict = {}
            vs_dict['label'] = marital

            for item in province_maritalstatus:
                if marital == item['marital_status']:
                    if "province" in vs_dict:
                        vs_dict['province'] = vs_dict['province'] + item['total']
                    else:
                        vs_dict["province"] = item['total']

            for item in pratinidhi_maritalstatus:
                if marital == item['marital_status']:
                    if "federal" in vs_dict:
                        vs_dict['federal'] = vs_dict['federal'] + item['total']
                    else:
                        vs_dict["federal"] = item['total']

            for item in national_maritalstatus:
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
        province_election_before = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'party_name', 'aaja_vanda_agadi_chunab_ladnu_vayeko_chha')\
        .distinct().annotate(total=Count('aaja_vanda_agadi_chunab_ladnu_vayeko_chha'))
        pratinidhi_election_before = PratinidhiShava.objects.values('province_id', 'party_name', 'aaja_vanda_agadi_chunab_ladnu_vayeko_chha')\
        .distinct().annotate(total=Count('aaja_vanda_agadi_chunab_ladnu_vayeko_chha'))
        national_election_before = RastriyaShava.objects.values('province_id', 'party_name', 'aaja_vanda_agadi_chunab_ladnu_vayeko_chha')\
        .distinct().annotate(total=Count('aaja_vanda_agadi_chunab_ladnu_vayeko_chha'))

        province_election_list = list(chain(province_election_before, pratinidhi_election_before, national_election_before))
 
        election_before_list = []
        for election_before in province_election_list:
            if election_before['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                elections = election_before['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']
                election_before_list.append(elections)

        election_before_set = set(election_before_list)

        province_election_before_list = []


        for election in election_before_set:
            province_dict = {}
            province_dict['label'] = election
            for item in province_election_list:
                if item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                    if election == item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                        if item['province_id'] in province_dict:
                            province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                        else:
                            province_dict[item['province_id']] = item['total']

            province_election_before_list.append(dict(province_dict))


        total_election_before_dict['provincial'] = province_election_before_list

        #for election experience on basis of political parties
        party_election_before = []

        for m in election_before_set:
            party_dict = {}
            party_dict['label'] = m
            for item in province_election_list:
                if item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                    if m == item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
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

            for item in province_election_before:
                if item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                    if elections == item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                        if "province" in vs_dict:
                            vs_dict['province'] = vs_dict['province'] + item['total']
                        else:
                            vs_dict["province"] = item['total']

            for item in pratinidhi_election_before:
                if item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                    if elections == item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                        if "federal" in vs_dict:
                            vs_dict['federal'] = vs_dict['federal'] + item['total']
                        else:
                            vs_dict["federal"] = item['total']

            for item in national_election_before:
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
        pratinidhi_party = PratinidhiShava.objects.values('province_id', 'party_name')\
        .distinct().annotate(total=Count('party_name'))
        national_party = RastriyaShava.objects.values('province_id', 'party_name')\
        .distinct().annotate(total=Count('party_name'))

        total_party_list = list(chain(province_party, pratinidhi_party, national_party))

        party_list = []
        for party in total_party_list:
            if party['party_name']:
                parties = party['party_name']
                party_list.append(parties)

        party_set = set(party_list)

        province_party_list = []

        for party in party_set:
            province_dict = {}
            province_dict['label'] = party
            for item in total_party_list:
                if item['party_name']:
                    if party == item['party_name']:
                        if item['province_id'] in province_dict:
                            province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                        else:
                            province_dict[item['province_id']] = item['total']

            province_party_list.append(dict(province_dict))


        total_party_dict['provincial'] = province_party_list

        #for parties on basis of nation, federal and province
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
            'party_name', 'nirwachit_chetra_pratiko_pratibadhata', 'province_id'
            )
        federal_political_commitment = PratinidhiShava.objects.values(
            'party_name', 'nirwachit_chetra_pratiko_pratibadhata', 'province_id'
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
            for item in commitment_lists:
                for i in item['nirwachit_chetra_pratiko_pratibadhata'].split(","):
                    if i.title().strip(" ") in commitment:
                        if item['province_id'] in province_dict:
                            province_dict[item['province_id']] = province_dict[item['province_id']] + 1
                        else:
                            province_dict[item['province_id']] = 1

            province_political_commitment_list.append(dict(province_dict))

        total_commitment_dict['provincial'] = province_political_commitment_list

        #for political commitments on basis of party
        party_political_commitment_list = []

        for commitment in commitment_set:
            party_dict = {}
            party_dict['label'] = commitment
            for item in commitment_lists:
                for i in item['nirwachit_chetra_pratiko_pratibadhata'].split(","):
                    if i.title().strip(" ") in commitment:
                        if item['party_name']:
                            if item['party_name'] in party_dict:
                                party_dict[item['party_name']] = party_dict[item['party_name']] + 1
                            else:
                                party_dict[item['party_name']] = 1

            party_political_commitment_list.append(dict(party_dict))

        total_commitment_dict['party'] = party_political_commitment_list


        vs = []
        for commitment in commitment_set:
            vs_dict = {}
            vs_dict['label'] = commitment
            vs_list = []

            for item in national_political_commitment:
                for i in item['nirwachit_chetra_pratiko_pratibadhata'].split(","):
                    if i.title().strip(" ") in commitment:
                        vs_list.append('national')

            for item in federal_political_commitment:
                for i in item['nirwachit_chetra_pratiko_pratibadhata'].split(","):
                    if i.title().strip(" ") in commitment:
                        vs_list.append('federal')

            for item in province_political_commitment:
                for i in item['nirwachit_chetra_pratiko_pratibadhata'].split(","):
                    if i.title().strip(" ") in commitment:
                        vs_list.append('province')

            total_arrays = np.array(np.unique(vs_list, return_counts=True)).T

            for total in total_arrays:
                vs_dict[total[0]] = total[1]

            vs.append(dict(vs_dict))

        total_commitment_dict['nationalvsfederalvsprovincial'] = vs

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

class LocalAgeViewSet(views.APIView):

    def get(self, request):
        ages = MahilaPratinidhiForm.objects.values('age')
        return Response(ages)

class NationalAgeViewSet(views.APIView):

    def get(self, request):
        ages = RastriyaShava.objects.values('age')
        return Response(ages)

class FederalAgeViewSet(views.APIView):

    def get(self, request):
        ages = PratinidhiShava.objects.values('age')
        return Response(ages)

class ProvinceAgeViewSet(views.APIView):

    def get(self, request):
        ages = ProvinceMahilaPratinidhiForm.objects.values('age')
        return Response(ages)

class CompareAllViewSet(views.APIView):

    def get(self, request, *args, **kwargs):
        container = {} #root dictionary
        age_list = [] #list to store dictionary of  hlcit1 and hlcit2
        age_dict = {} #dictionary to store ages of hlcit1 and hlcit2
        hlcit1_list = [] #stores ages of hlcit1
        hlcit2_list = [] #stores ages of hlcit2

        national_age_1 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('age')
        federal_age_1 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('age')
        province_age_1 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('age')
        local_age_1 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('age')

        hlcit1_age = chain(national_age_1, federal_age_1, province_age_1, local_age_1) #dictionary of ages of hlcit1
        for age in hlcit1_age:
            hlcit1_list.append(int(float(age['age'])))

        age_dict['hlcit1'] = hlcit1_list

        national_age_2 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('age')
        federal_age_2 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('age')
        province_age_2 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('age')
        local_age_2 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('age')

        hlcit2_age = chain(national_age_2, federal_age_2, province_age_2, local_age_2)
        for age in hlcit2_age:
            hlcit2_list.append(int(float(age['age'])))

        age_dict['hlcit2'] = hlcit2_list

        age_list.append(age_dict)

        #for EDUCATION
        national_education_1 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('educational_qualification') \
            .distinct().annotate(total=Count('educational_qualification'))
        federal_education_1 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('educational_qualification') \
            .distinct().annotate(total=Count('educational_qualification'))
        province_education_1 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('educational_qualification') \
            .distinct().annotate(total=Count('educational_qualification'))
        local_education_1 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('educational_qualification') \
            .distinct().annotate(total=Count('educational_qualification'))

        national_education_2 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('educational_qualification') \
            .distinct().annotate(total=Count('educational_qualification'))
        federal_education_2 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('educational_qualification') \
            .distinct().annotate(total=Count('educational_qualification'))
        province_education_2 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('educational_qualification') \
            .distinct().annotate(total=Count('educational_qualification'))
        local_education_2 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('educational_qualification') \
            .distinct().annotate(total=Count('educational_qualification'))

        hlcit1_education = chain(national_education_1, federal_education_1, province_education_1, local_education_1)
        hlcit2_educaition = chain(national_education_2, federal_education_2, province_education_2, local_education_2)

        totals = [] #total education labels in both hlcits' eg: [Literature, Literature, Post Graduate]
        totals1 =[] #total labels in hlcit1 eg: [Literature]
        totals2 = [] #total labels in hlcit2 eg: [Literature, Post Graduate]

        for education in hlcit1_education:
            if education['educational_qualification']:
                totals.append(education['educational_qualification'])
                totals1.append(education['educational_qualification'])

        for education in hlcit2_educaition:
            if education['educational_qualification']:
                totals.append(education['educational_qualification'])
                totals2.append(education['educational_qualification'])

        education_labels = np.unique(totals) #unique lables of total labels eg: [Literature, Post Graduate]
        lbl_list = [] #list to hold each dictionary with different education labels
        for edu in education_labels:
            dictt ={}
            coun1 = 0
            coun2 = 0
            dictt['label'] = edu
            for educat in totals1:
                if educat == edu:
                    coun1 = coun1 + 1
            for educat in totals2:
                if educat == edu:
                    coun2 = coun2 + 1
            dictt['hlcit1'] = coun1
            dictt['hlcit2'] = coun2
            lbl_list.append(dictt)

        #for years in political party
        year_list = []  # list to store dictionary of  hlcit1 and hlcit2
        year_dict = {}  # dictionary to store ages of hlcit1 and hlcit2
        hlcit1_list_year = []  # stores ages of hlcit1
        hlcit2_list_year = []  # stores ages of hlcit2

        national_year_1 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_joined_date')
        federal_year_1 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_joined_date')
        province_year_1 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_joined_date')
        local_year_1 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_joined_date')

            hlcit1_year = chain(national_year_1, federal_year_1, province_year_1,local_year_1)  # dictionary of ages of hlcit1

            # import datetime
            # now = datetime.datetime.now()
            # yr = 2019
            # current = 0
            # nepp = 0
            #
            # while (yr == 2019):
            #     nepp = nepp+2075
            #     current = now.year
            #     if current > yr:
            #         nepp += 1
            #
            # print("year: ", yr)
            # print("current: ", current)
            # print("nepali: ", nepp)


        for year in hlcit1_year:
            if year['party_joined_date']:
                hlcit1_list_year.append(2075 - int(float(year['party_joined_date'])))
        year_dict['hlcit1'] = hlcit1_list_year

        national_year_2 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_joined_date')
        federal_year_2 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_joined_date')
        province_year_2 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_joined_date')
        local_year_2 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_joined_date')

        hlcit2_year = chain(national_year_2, federal_year_2, province_year_2, local_year_2)
        # for year in hlcit2_year:
        #     hlcit2_list.append(int(float(year['political_engagement'])))

        for year in hlcit2_year:
            if year['party_joined_date']:
                hlcit2_list_year.append(2075 - int(float(year['party_joined_date'])))
        year_dict['hlcit2'] = hlcit2_list_year

        year_list.append(year_dict)

        # for Ethnicity
        national_caste_1 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        federal_caste_1 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        province_caste_1 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        local_caste_1 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('caste') \
            .distinct().annotate(total=Count('caste'))

        national_caste_2 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        federal_caste_2 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        province_caste_2 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        local_caste_2 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('caste') \
            .distinct().annotate(total=Count('caste'))

        hlcit1_caste = chain(national_caste_1, federal_caste_1, province_caste_1, local_caste_1)
        hlcit2_caste = chain(national_caste_2, federal_caste_2, province_caste_2,
                                    local_caste_2)

        totals_caste = []  # total education labels in both hlcits' eg: [Literature, Literature, Post Graduate]
        totals1_caste = []  # total labels in hlcit1 eg: [Literature]
        totals2_caste = []  # total labels in hlcit2 eg: [Literature, Post Graduate]

        for caste in hlcit1_caste:
            if caste['caste']:
                totals_caste.append(caste['caste'])
                totals1_caste.append(caste['caste'])

        for caste in hlcit2_caste:
            if caste['caste']:
                totals_caste.append(caste['caste'])
                totals2_caste.append(caste['caste'])

        caste_labels = np.unique(totals_caste)  # unique lables of total labels eg: [Literature, Post Graduate]
        lbl_list_caste = []  # list to hold each dictionary with different education labels
        for cas in caste_labels:
            dictt = {}
            coun1 = 0
            coun2 = 0
            dictt['label'] = cas
            for cast in totals1_caste:
                print("educat: ", cast)
                if cast == cas:
                    coun1 = coun1 + 1
            for cast in totals2_caste:
                if cast == cas:
                    coun2 = coun2 + 1
            dictt['hlcit1'] = coun1
            dictt['hlcit2'] = coun2
            lbl_list_caste.append(dictt)

        # for Party Name
        national_party_name_1 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_name') \
            .distinct().annotate(total=Count('party_name'))
        federal_party_name_1 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_name') \
            .distinct().annotate(total=Count('party_name'))
        province_party_name_1 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values(
            'party_name') \
            .distinct().annotate(total=Count('party_name'))
        local_party_name_1 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_name') \
            .distinct().annotate(total=Count('party_name'))

        national_party_name_2 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_name') \
            .distinct().annotate(total=Count('party_name'))
        federal_party_name_2 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_name') \
            .distinct().annotate(total=Count('party_name'))
        province_party_name_2 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values(
            'party_name') \
            .distinct().annotate(total=Count('party_name'))
        local_party_name_2 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_name') \
            .distinct().annotate(total=Count('party_name'))

        hlcit1_party_name = chain(national_party_name_1, federal_party_name_1, province_party_name_1, local_party_name_1)
        hlcit2_party_name = chain(national_party_name_2, federal_party_name_2, province_party_name_2, local_party_name_2)

        totals_party_name = []  # total education labels in both hlcits' eg: [Literature, Literature, Post Graduate]
        totals1_party_name = []  # total labels in hlcit1 eg: [Literature]
        totals2_party_name = []  # total labels in hlcit2 eg: [Literature, Post Graduate]

        for party_name in hlcit1_party_name:
            if party_name['party_name']:
                totals_party_name.append(party_name['party_name'])
                totals1_party_name.append(party_name['party_name'])

        for party_name in hlcit2_party_name:
            if party_name['party_name']:
                totals_party_name.append(party_name['party_name'])
                totals2_party_name.append(party_name['party_name'])

        party_name_labels = np.unique(totals_party_name)  # unique lables of total labels eg: [Literature, Post Graduate]
        lbl_list_party_name = []  # list to hold each dictionary with different education labels
        for par in party_name_labels:
            dictt = {}
            coun1 = 0
            coun2 = 0
            dictt['label'] = par
            for part in totals1_party_name:
                print("educat: ", part)
                if part == par:
                    coun1 = coun1 + 1
            for part in totals2_party_name:
                if part == par:
                    coun2 = coun2 + 1
            dictt['hlcit1'] = coun1
            dictt['hlcit2'] = coun2
            lbl_list_party_name.append(dictt)

        container['age'] = age_list
        container['education'] = lbl_list
        container['Years in Politics'] = year_list
        container['Ethnicity'] = lbl_list_caste
        container['Party Name'] = lbl_list_party_name
        
        return Response(container)

def common(self, basis, para1, para2):
    container = {}  # root dictionary
    age_list = []  # list to store dictionary of  hlcit1 and hlcit2
    age_dict = {}  # dictionary to store ages of hlcit1 and hlcit2
    hlcit1_list = []  # stores ages of hlcit1
    hlcit2_list = []  # stores ages of hlcit2

    national_age_1 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('age')
    federal_age_1 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('age')
    province_age_1 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('age')
    local_age_1 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('age')

    hlcit1_age = chain(national_age_1, federal_age_1, province_age_1, local_age_1)  # dictionary of ages of hlcit1
    for age in hlcit1_age:
        hlcit1_list.append(int(float(age['age'])))

    age_dict['hlcit1'] = hlcit1_list

    national_age_2 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('age')
    federal_age_2 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('age')
    province_age_2 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('age')
    local_age_2 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('age')

    hlcit2_age = chain(national_age_2, federal_age_2, province_age_2, local_age_2)
    for age in hlcit2_age:
        hlcit2_list.append(int(float(age['age'])))

    age_dict['hlcit2'] = hlcit2_list

    age_list.append(age_dict)

    # for EDUCATION
    national_education_1 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values(
        'educational_qualification') \
        .distinct().annotate(total=Count('educational_qualification'))
    federal_education_1 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values(
        'educational_qualification') \
        .distinct().annotate(total=Count('educational_qualification'))
    province_education_1 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values(
        'educational_qualification') \
        .distinct().annotate(total=Count('educational_qualification'))
    local_education_1 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values(
        'educational_qualification') \
        .distinct().annotate(total=Count('educational_qualification'))

    national_education_2 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values(
        'educational_qualification') \
        .distinct().annotate(total=Count('educational_qualification'))
    federal_education_2 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values(
        'educational_qualification') \
        .distinct().annotate(total=Count('educational_qualification'))
    province_education_2 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values(
        'educational_qualification') \
        .distinct().annotate(total=Count('educational_qualification'))
    local_education_2 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values(
        'educational_qualification') \
        .distinct().annotate(total=Count('educational_qualification'))

    hlcit1_education = chain(national_education_1, federal_education_1, province_education_1, local_education_1)
    hlcit2_educaition = chain(national_education_2, federal_education_2, province_education_2, local_education_2)

    totals = []  # total education labels in both hlcits' eg: [Literature, Literature, Post Graduate]
    totals1 = []  # total labels in hlcit1 eg: [Literature]
    totals2 = []  # total labels in hlcit2 eg: [Literature, Post Graduate]

    for education in hlcit1_education:
        if education['educational_qualification']:
            totals.append(education['educational_qualification'])
            totals1.append(education['educational_qualification'])

    for education in hlcit2_educaition:
        if education['educational_qualification']:
            totals.append(education['educational_qualification'])
            totals2.append(education['educational_qualification'])

    education_labels = np.unique(totals)  # unique lables of total labels eg: [Literature, Post Graduate]
    lbl_list = []  # list to hold each dictionary with different education labels
    for edu in education_labels:
        dictt = {}
        coun1 = 0
        coun2 = 0
        dictt['label'] = edu
        for educat in totals1:
            if educat == edu:
                coun1 = coun1 + 1
        for educat in totals2:
            if educat == edu:
                coun2 = coun2 + 1
        dictt['hlcit1'] = coun1
        dictt['hlcit2'] = coun2
        lbl_list.append(dictt)

        # for years in political party
        year_list = []  # list to store dictionary of  hlcit1 and hlcit2
        year_dict = {}  # dictionary to store ages of hlcit1 and hlcit2
        hlcit1_list_year = []  # stores ages of hlcit1
        hlcit2_list_year = []  # stores ages of hlcit2

        national_year_1 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_joined_date')
        federal_year_1 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_joined_date')
        province_year_1 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values(
            'party_joined_date')
        local_year_1 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_joined_date')

        hlcit1_year = chain(national_year_1, federal_year_1, province_year_1,
                            local_year_1)  # dictionary of ages of hlcit1

        # import datetime
        # now = datetime.datetime.now()
        # yr = 2019
        # current = 0
        # nepp = 0
        #
        # while (yr == 2019):
        #     nepp = nepp+2075
        #     current = now.year
        #     if current > yr:
        #         nepp += 1
        #
        # print("year: ", yr)
        # print("current: ", current)
        # print("nepali: ", nepp)

        for year in hlcit1_year:
            if year['party_joined_date']:
                hlcit1_list_year.append(2075 - int(float(year['party_joined_date'])))
        year_dict['hlcit1'] = hlcit1_list_year

        national_year_2 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_joined_date')
        federal_year_2 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_joined_date')
        province_year_2 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values(
            'party_joined_date')
        local_year_2 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_joined_date')

        hlcit2_year = chain(national_year_2, federal_year_2, province_year_2, local_year_2)
        # for year in hlcit2_year:
        #     hlcit2_list.append(int(float(year['political_engagement'])))

        for year in hlcit2_year:
            if year['party_joined_date']:
                hlcit2_list_year.append(2075 - int(float(year['party_joined_date'])))
        year_dict['hlcit2'] = hlcit2_list_year

        year_list.append(year_dict)

        # for Ethnicity
        national_caste_1 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        federal_caste_1 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        province_caste_1 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        local_caste_1 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('caste') \
            .distinct().annotate(total=Count('caste'))

        national_caste_2 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        federal_caste_2 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        province_caste_2 = ProvinceMahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('caste') \
            .distinct().annotate(total=Count('caste'))
        local_caste_2 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('caste') \
            .distinct().annotate(total=Count('caste'))

        hlcit1_caste = chain(national_caste_1, federal_caste_1, province_caste_1, local_caste_1)
        hlcit2_caste = chain(national_caste_2, federal_caste_2, province_caste_2,
                             local_caste_2)

        totals_caste = []  # total education labels in both hlcits' eg: [Literature, Literature, Post Graduate]
        totals1_caste = []  # total labels in hlcit1 eg: [Literature]
        totals2_caste = []  # total labels in hlcit2 eg: [Literature, Post Graduate]

        for caste in hlcit1_caste:
            if caste['caste']:
                totals_caste.append(caste['caste'])
                totals1_caste.append(caste['caste'])

        for caste in hlcit2_caste:
            if caste['caste']:
                totals_caste.append(caste['caste'])
                totals2_caste.append(caste['caste'])

        caste_labels = np.unique(totals_caste)  # unique lables of total labels eg: [Literature, Post Graduate]
        lbl_list_caste = []  # list to hold each dictionary with different education labels
        for cas in caste_labels:
            dictt = {}
            coun1 = 0
            coun2 = 0
            dictt['label'] = cas
            for cast in totals1_caste:
                print("educat: ", cast)
                if cast == cas:
                    coun1 = coun1 + 1
            for cast in totals2_caste:
                if cast == cas:
                    coun2 = coun2 + 1
            dictt['hlcit1'] = coun1
            dictt['hlcit2'] = coun2
            lbl_list_caste.append(dictt)

            # for Party Name
            national_party_name_1 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_name') \
                .distinct().annotate(total=Count('party_name'))
            federal_party_name_1 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit1']).values('party_name') \
                .distinct().annotate(total=Count('party_name'))
            province_party_name_1 = ProvinceMahilaPratinidhiForm.objects.filter(
                hlcit_code=self.kwargs['hlcit1']).values(
                'party_name') \
                .distinct().annotate(total=Count('party_name'))
            local_party_name_1 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit1']).values(
                'party_name') \
                .distinct().annotate(total=Count('party_name'))

            national_party_name_2 = RastriyaShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_name') \
                .distinct().annotate(total=Count('party_name'))
            federal_party_name_2 = PratinidhiShava.objects.filter(hlcit_code=self.kwargs['hlcit2']).values('party_name') \
                .distinct().annotate(total=Count('party_name'))
            province_party_name_2 = ProvinceMahilaPratinidhiForm.objects.filter(
                hlcit_code=self.kwargs['hlcit2']).values(
                'party_name') \
                .distinct().annotate(total=Count('party_name'))
            local_party_name_2 = MahilaPratinidhiForm.objects.filter(hlcit_code=self.kwargs['hlcit2']).values(
                'party_name') \
                .distinct().annotate(total=Count('party_name'))

            hlcit1_party_name = chain(national_party_name_1, federal_party_name_1, province_party_name_1,
                                      local_party_name_1)
            hlcit2_party_name = chain(national_party_name_2, federal_party_name_2, province_party_name_2,
                                      local_party_name_2)

            totals_party_name = []  # total education labels in both hlcits' eg: [Literature, Literature, Post Graduate]
            totals1_party_name = []  # total labels in hlcit1 eg: [Literature]
            totals2_party_name = []  # total labels in hlcit2 eg: [Literature, Post Graduate]

            for party_name in hlcit1_party_name:
                if party_name['party_name']:
                    totals_party_name.append(party_name['party_name'])
                    totals1_party_name.append(party_name['party_name'])

            for party_name in hlcit2_party_name:
                if party_name['party_name']:
                    totals_party_name.append(party_name['party_name'])
                    totals2_party_name.append(party_name['party_name'])

            party_name_labels = np.unique(
                totals_party_name)  # unique lables of total labels eg: [Literature, Post Graduate]
            lbl_list_party_name = []  # list to hold each dictionary with different education labels
            for par in party_name_labels:
                dictt = {}
                coun1 = 0
                coun2 = 0
                dictt['label'] = par
                for part in totals1_party_name:
                    print("educat: ", part)
                    if part == par:
                        coun1 = coun1 + 1
                for part in totals2_party_name:
                    if part == par:
                        coun2 = coun2 + 1
                dictt['hlcit1'] = coun1
                dictt['hlcit2'] = coun2
                lbl_list_party_name.append(dictt)

    container['age'] = age_list
    container['education'] = lbl_list
    container['Years in Politics'] = year_list
    container['Ethnicity'] = lbl_list_caste
    container['Party Name'] = lbl_list_party_name
    return Response(container)