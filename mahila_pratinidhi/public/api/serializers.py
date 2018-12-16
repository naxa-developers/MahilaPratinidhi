from rest_framework import serializers

from core.models import RastriyaShava, PratinidhiShava, ProvinceMahilaPratinidhiForm, MahilaPratinidhiForm, District

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

class MapSerializers(serializers.ListSerializer):
    map_data = serializers.DictField()


class AgeSerializers(serializers.ListSerializer):
    total_age = serializers.ListField()
    provinces_average_age = serializers.ListField()
    province = serializers.ListField()
    nationale = serializers.ListField()
    federal= serializers.ListField()


class EthnicitySerializers(serializers.ListSerializer):
    ethnicity_data = serializers.DictField()


class MotherTongueSerializers(serializers.ListSerializer):
    mother_tongue = serializers.DictField()

class EducationSerializers(serializers.ListSerializer):
    educational_qualification = serializers.DictField()


class PoliticalEngagementSerializers(serializers.ListSerializer):
    political_engagement = serializers.DictField()


class ElectionTypeSerializers(serializers.ListSerializer):
    election_type = serializers.DictField()


class MaritalStatusSerializers(serializers.ListSerializer):
    marital_status = serializers.DictField()


class ElectionExperienceSerializers(serializers.ListSerializer):
    election_before = serializers.DictField()


class PartySerializers(serializers.ListSerializer):
    party = serializers.DictField()


class CommitmentSerializers(serializers.ListSerializer):
    commitment = serializers.DictField()


class DistrictsSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ('elected_women', )

class RastriyaSerialiser(serializers.ModelSerializer):
    class_name = serializers.SerializerMethodField()

    def get_class_name(self, obj):
        return obj.__class__.__name__

    class Meta:
        model = RastriyaShava
        fields = ('id', 'english_name', 'class_name')


class PratinidhiSerializer(serializers.ModelSerializer):
    class_name = serializers.SerializerMethodField()

    def get_class_name(self, obj):
        return obj.__class__.__name__

    class Meta:
        model = PratinidhiShava
        fields = ('id', 'english_name', 'class_name')


class ProvinceSerializer(serializers.ModelSerializer):
    class_name = serializers.SerializerMethodField()

    def get_class_name(self, obj):
        return obj.__class__.__name__

    class Meta:
        model = ProvinceMahilaPratinidhiForm
        fields = ('id', 'english_name', 'class_name')


class HlcitSerializer(serializers.Serializer):
    class_name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'class_name')

    def get_name(self, obj):
        return obj.name

    def get_id(slef,obj):
        return obj.id

    def get_class_name(self, obj):
        return obj.__class__.__name__


