from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import status, serializers, views
from rest_framework.response import Response
import json
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize

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
        
        for ages in rastriya_age:
            if ages['age'] != "":
                age.append(ages['age'])
            
        
        for ages in pratinidhi_age:
            if ages['age'] != "":
                age.append(ages['age'])
        
        for ages in provincial_age:
            if ages['age'] != "":
                age.append(ages['age'])
        
        # for ages in local_age:
        #     if ages['age'] != "":
        #         age.append(ages['age'])
        
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
        data = []
        ethnicity={}
        ethnicity.fromkeys({"caste"})
        print(ethnicity)

        # rastriya_caste = RastriyaShava.objects.values('caste').annotate(Count('caste'))\
        # .annotate(total=Sum('id'))

        pratinidhi_caste = PratinidhiShava.objects.values('caste').annotate(Count('caste'))\
        .annotate(total=Count('id'))
        print(pratinidhi_caste)

        provincial_caste = ProvinceMahilaPratinidhiForm.objects.values('caste').annotate(Count('caste'))\
        .annotate(total=Count('id'))
        # local_caste = MahilaPratinidhiForm.objects.values('caste')
        
        # for castes in rastriya_caste:
        #     if not castes['caste'] in ethnicity['caste']:
        #         ethnicity['caste']=castes['caste']
        #         ethnicity[castes['caste']]['total']=castes['total']
            
        #     else:
        #         ethnicity[castes['caste']]['total'] += castes['total']
            
        
        for castes in pratinidhi_caste:
            ethnicity['caste'] = castes['caste']
            ethnicity['total'] = castes['total']
            data.append(ethnicity.copy)
        
        for castes in provincial_caste:
            for count in range(len(data)):
                if not castes['caste'] in data[count]['caste']:
                    ethnicity['caste'] = castes['caste']
                    ethnicity['total'] = castes['total']
                    data.append(ethnicity.copy)
            
                else:
                    data[count]['total'] += castes['total']
        
        # for castes in rastriya_caste:
        #     if not castes['caste'] in ethnicity['caste']:
            #     ethnicity['caste']=castes['caste']
            #     ethnicity['total']=castes['total']
            
            # else:
            #     ethnicity['total'] += castes['total']
        
        return Response(ethnicity)




