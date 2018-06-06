from django.forms import widgets
from rest_framework import serializers
from ModuleCommunicator.models import *


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    module_name = serializers.CharField(source='get_module_name', read_only=True)

    class Meta:
        model = ResultModel
        fields = ('module_name', 'module_result')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = ImageModel
        fields = ('image', 'modules', 'token', 'uploaded_date', 'updated_date', 'results')
        read_only_fields = ('token', 'uploaded_date', 'updated_date', 'results')

