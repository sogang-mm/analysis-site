from django.forms import widgets
from rest_framework import serializers
from ModuleCommunicator.models import *


class ResultDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResultDetailModel
        fields = ('x', 'y', 'w', 'h', 'values', 'debug')


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    module_name = serializers.CharField(source='get_module_name', read_only=True)
    module_result = ResultDetailSerializer(many=True, read_only=True)

    class Meta:
        model = ResultModel
        fields = ('module_name', 'module_result', 'debug')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = ImageModel
        fields = ('image', 'modules', 'token', 'uploaded_date', 'updated_date', 'results', 'debug')
        read_only_fields = ('token', 'uploaded_date', 'updated_date', 'results', 'debug')

