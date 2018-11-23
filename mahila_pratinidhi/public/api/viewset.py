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
        pra_age = []
        age=[]
        rastriya_age = RastriyaShava.objects.values('age')
        pratinidhi_age = PratinidhiShava.objects.values('age')
        provincial_age = ProvinceMahilaPratinidhiForm.objects.values('age')
        local_age = MahilaPratinidhiForm.objects.values('age')

        for ages in rastriya_age:
            if ages['age'] != "":
                age.append(ages['age'])
            
        
        for ages in pratinidhi_age:
            if ages['age'] != "":
                age.append(ages['age'])
        
        for ages in provincial_age:
            if ages['age'] != "":
                pra_age.append(ages['age'])
                age.append(ages['age'])
        
        for ages in local_age:
            if ages['age'] != "":
                age.append(ages['age'])
        

        data = {'total_age':age, 'pratinidhi_age':pra_age}
        return Response(data)
        





