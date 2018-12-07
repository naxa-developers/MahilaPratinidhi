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
from core.models import RastriyaShava, PratinidhiShava, ProvinceMahilaPratinidhiForm, MahilaPratinidhiForm, Province, District
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
        map_api = {}
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

        map_api['all'] = maps

        #for national lists
        national_dict = {}
        national_province_dict = {}

        national_province = Province.objects.values('name').annotate(total=Count('rastriyashava'))

        for item in national_province:
            national_province_dict[item['name']] = item['total']
        national_dict['province'] = national_province_dict

        national_district_dict = {}
        national_district = RastriyaShava.objects.values('permanent_address').annotate(total=Count('permanent_address'))

        for item in national_district:
            national_district_dict[item['permanent_address']] = item['total']
        national_dict['district'] = national_district_dict

        map_api['national']=national_dict

        #for federal lists
        federal_dict = {}
        federal_province_dict = {}

        federal_province = Province.objects.values('name').annotate(total=Count('pratinidhishava'))

        for item in federal_province:
            federal_province_dict[item['name']] = item['total']
        federal_dict['province'] = federal_province_dict

        federal_district_dict = {}
        federal_district = PratinidhiShava.objects.values('permanent_address').annotate(total=Count('permanent_address'))

        for item in federal_district:
            federal_district_dict[item['permanent_address']] = item['total']
        federal_dict['district'] = federal_district_dict

        map_api['federal']=federal_dict

        #for provincial lists
        provincial_dict = {}
        provincial_province_dict = {}

        provincial_province = Province.objects.values('name').annotate(total=Count('pratinidhishava'))

        for item in provincial_province:
            provincial_province_dict[item['name']] = item['total']
        provincial_dict['province'] = provincial_province_dict

        provincial_district_dict = {}
        provincial_district = ProvinceMahilaPratinidhiForm.objects.values('permanent_address').annotate(total=Count('permanent_address'))

        for item in provincial_district:
            provincial_district_dict[item['permanent_address']] = item['total']
        provincial_dict['district'] = provincial_district_dict

        map_api['provincial'] = provincial_dict


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
                if age['age'] in r:
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
                if age['age'] in r:
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
                if age['age'] in r:
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

        castes = list(chain(pratinidhi_caste, provincial_caste))
        totals = []
        for caste in castes:
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
            caste = provinces['caste']
            castes.append(caste)

        caste_set = set(castes)

        province_ethinicity=[]


        for caste in caste_set:
            province_dict = {}
            province_dict['label'] = caste
            for item in province_caste:
                if caste in item['caste']:
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

        party_caste = list(chain(province_party_caste, pratinidhi_party_caste))

        castes = []
        for item in party_caste:
            caste = item['caste']
            castes.append(caste)

        caste_set = set(castes)

        party_ethinicity=[]

        for caste in caste_set:
            party_dict = {}
            party_dict['label'] = caste
            for item in party_caste:
                if caste in item['caste']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']

            party_ethinicity.append(dict(party_dict))

        total_ethnicity['party'] = party_ethinicity

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
            mother_tongue['label'] = total[0]
            mother_tongue['total'] = total[1]

            data.append(dict(mother_tongue))

        total_mother_tongue['total'] = data

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
            province_dict['label'] = language
            for item in province_mother_tongue:
                if language in item['mother_tongue']:
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

        party_lang = list(chain(province_party_lang, pratinidhi_party_lang))

        languages = []
        for item in party_lang:
            lang = item['mother_tongue']
            languages.append(lang)

        language_set = set(languages)

        party_language=[]

        for language in language_set:
            party_dict = {}
            party_dict['label'] = language
            for item in party_lang:
                if language in item['mother_tongue']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']

            party_language.append(dict(party_dict))

        total_mother_tongue['party'] = party_language

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
            edu['label'] = total[0]
            edu['total'] = total[1]

            data.append(dict(edu))

        total_education['total'] = data

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
            province_dict['label'] = education
            for item in province_education:
                if education in item['educational_qualification']:
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

        party_edu = list(chain(province_party_edu, pratinidhi_party_edu))

        educations = []
        for item in party_edu:
            edu = item['educational_qualification']
            educations.append(edu)

        education_set = set(educations)

        party_education=[]

        for education in education_set:
            party_dict = {}
            party_dict['label'] = education
            for item in party_edu:
                if education in item['educational_qualification']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']

            party_education.append(dict(party_dict))

        total_education['party'] = party_education

        return Response(total_education)


class ElectionTypeViewSet(views.APIView):

    def get(self, request):

        total_election_type = {}
        data = []
        election_type={}

        #for total educational qualification
        pratinidhi = PratinidhiShava.objects.all()
        provincial = ProvinceMahilaPratinidhiForm.objects.all()

        election_types = list(chain(pratinidhi, provincial))
        totals = []
        for election in election_types:
            totals.append(election.nirwachit_prakriya)

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            election_type['label'] = total[0]
            election_type['total'] = total[1]

            data.append(dict(election_type))

        total_election_type['total'] = data

        #for educational qualification on basis of provinces
        province_election = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'nirwachit_prakriya')\
        .distinct().annotate(total=Count('nirwachit_prakriya'))
        election_types = []
        for election in province_election:
            elec = election['nirwachit_prakriya']
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

        #for ethnicities on basis of political parties
        province_party_election = ProvinceMahilaPratinidhiForm.objects.values('party_name', 'nirwachit_prakriya')\
        .distinct().annotate(total=Count('nirwachit_prakriya'))
        pratinidhi_party_election = PratinidhiShava.objects.values('party_name', 'nirwachit_prakriya')\
        .distinct().annotate(total=Count('nirwachit_prakriya'))

        party_election = list(chain(province_party_election, pratinidhi_party_election))

        elections = []
        for item in party_election:
            elect = item['nirwachit_prakriya']
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

        return Response(total_election_type)


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


class MaritalStatusViewSet(views.APIView):

    def get(self, request):

        total_maritalstatus_dict = {}
        data_list = []
        maritalstatus_dict = {}

        #for total educational qualification
        pratinidhi = PratinidhiShava.objects.all()
        provincial = ProvinceMahilaPratinidhiForm.objects.all()

        maritalstatus_list = list(chain(pratinidhi, provincial))
        totals = []
        for marital in maritalstatus_list:
            totals.append(marital.marital_status)

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            maritalstatus_dict['label'] = total[0]
            maritalstatus_dict['total'] = total[1]

            data_list.append(dict(maritalstatus_dict))

        total_maritalstatus_dict['total'] = data_list

        #for educational qualification on basis of provinces
        province_maritalstatus = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'marital_status')\
        .distinct().annotate(total=Count('marital_status'))
        marital_status_list = []
        for marital in province_maritalstatus:
            maritals = marital['marital_status']
            marital_status_list.append(maritals)

        marital_status_set = set(marital_status_list)

        province_marital_list = []


        for marital in marital_status_set:
            province_dict = {}
            province_dict['label'] = marital
            for item in province_maritalstatus:
                if marital in item['marital_status']:
                    if str(item['province_id']) in province_dict:
                        province_dict[item['province_id']] = province_dict[item['province_id']] + item['total']
                    else:
                        province_dict[item['province_id']] = item['total']

            province_marital_list.append(dict(province_dict))


        total_maritalstatus_dict['provincial'] = province_marital_list

        #for ethnicities on basis of political parties
        province_party_marital = ProvinceMahilaPratinidhiForm.objects.values('party_name', 'marital_status')\
        .distinct().annotate(total=Count('marital_status'))
        pratinidhi_party_marital = PratinidhiShava.objects.values('party_name', 'marital_status')\
        .distinct().annotate(total=Count('marital_status'))

        party_marital =  list(chain(province_party_marital, pratinidhi_party_marital))

        marital_list = []
        for item in party_marital:
            marital = item['marital_status']
            marital_list.append(marital)

        marital_set = set(marital_list)

        party_marital_list = []

        for m in marital_set:
            party_dict = {}
            party_dict['label'] = m
            for item in party_marital:
                if m in item['marital_status']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']

            party_marital_list.append(dict(party_dict))

        total_maritalstatus_dict['party'] = party_marital_list

        return Response(total_maritalstatus_dict)


class ElectionParticipate(views.APIView):

    def get(self, request):
        total_election_before_dict = {}
        data_list = []
        election_before_dict = {}

        #for total educational qualification
        pratinidhi = PratinidhiShava.objects.all()
        provincial = ProvinceMahilaPratinidhiForm.objects.all()

        election_before_list = list(chain(pratinidhi, provincial))
        totals = []
        for elect in election_before_list:
            totals.append(elect.aaja_vanda_agadi_chunab_ladnu_vayeko_chha)

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            election_before_dict['label'] = total[0]
            election_before_dict['total'] = total[1]

            data_list.append(dict(election_before_dict))

        total_election_before_dict['total'] = data_list

        #for educational qualification on basis of provinces
        province_election_before = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'aaja_vanda_agadi_chunab_ladnu_vayeko_chha')\
        .distinct().annotate(total=Count('aaja_vanda_agadi_chunab_ladnu_vayeko_chha'))
        election_before_list = []
        for election_before in province_election_before:
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

        #for ethnicities on basis of political parties
        province_party_election_before = ProvinceMahilaPratinidhiForm.objects\
        .values('party_name', 'aaja_vanda_agadi_chunab_ladnu_vayeko_chha')\
        .distinct().annotate(total=Count('aaja_vanda_agadi_chunab_ladnu_vayeko_chha'))
        pratinidhi_party_election_before = PratinidhiShava.objects\
        .values('party_name', 'aaja_vanda_agadi_chunab_ladnu_vayeko_chha')\
        .distinct().annotate(total=Count('aaja_vanda_agadi_chunab_ladnu_vayeko_chha'))

        party_election_before_list =  list(
            chain(
                province_party_election_before, pratinidhi_party_election_before))

        election_before_list = []
        for item in party_election_before_list:
            election_before = item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']
            election_before_list.append(election_before)

        election_before_set = set(election_before_list)

        party_election_before = []

        for m in election_before_set:
            party_dict = {}
            party_dict['label'] = m
            for item in party_election_before_list:
                if m in item['aaja_vanda_agadi_chunab_ladnu_vayeko_chha']:
                    if item['party_name'] in party_dict:
                        party_dict[item['party_name']] = party_dict[item['party_name']] + item['total']
                    else:
                        party_dict[item['party_name']] = item['total']

            party_election_before.append(dict(party_dict))

        total_election_before_dict['party'] = party_election_before

        return Response(total_election_before_dict)


class PartyViewSet(views.APIView):

    def get(self, request):

        total_party_dict = {}
        data_list = []
        party_dict = {}

        #for total educational qualification
        pratinidhi = PratinidhiShava.objects.all()
        provincial = ProvinceMahilaPratinidhiForm.objects.all()

        party_list = list(chain(pratinidhi, provincial))
        totals = []
        for party in party_list:
            totals.append(party.party_name)

        total_arrays = np.array(np.unique(totals, return_counts=True)).T

        for total in total_arrays:
            party_dict['label'] = total[0]
            party_dict['total'] = total[1]

            data_list.append(dict(party_dict))

        total_party_dict['total'] = data_list

        province_party = ProvinceMahilaPratinidhiForm.objects.values('province_id', 'party_name')\
        .distinct().annotate(total=Count('party_name'))
        party_list = []
        for party in province_party:
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

        return Response(total_party_dict)
