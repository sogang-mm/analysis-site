from django.forms import widgets
from rest_framework import serializers
from AnalysisModules.models import *


class ModulesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ModulesModel
        fields = ('name', 'url', 'description', 'status')
        # read_only_fields = ('name', 'url', 'description', 'status')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('image', 'modules', 'token', 'uploaded_date', 'updated_date', 'result')
        read_only_fields = ('token', 'uploaded_date', 'updated_date', 'result')


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResultModel
        fields = ('module_name', 'result')
        read_only_fields = ('module_name', 'result')