from rest_framework import serializers

from core.models import RastriyaShava, PratinidhiShava, ProvinceMahilaPratinidhiForm, MahilaPratinidhiForm

class RastriyaShavaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RastriyaShava
        fields = '__all__'


class PratinidhiShavaSerializer(serializers.ModelSerializer):

    class Meta:
        model = PratinidhiShava
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProvinceMahilaPratinidhiForm
        fields = '__all__'


class LocalMahilaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MahilaPratinidhiForm
        fields = '__all__'

class AgeSerializers(serializers.ListSerializer):
    total_age = serializers.ListField()
    pratinidhi_age = serializers.ListField()

    


