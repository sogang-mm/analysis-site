from django.forms import widgets
from rest_framework import serializers
from ModuleCommunicator.models import *


class ResultDetailPositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResultDetailPositionModel
        fields = ('x', 'y', 'w', 'h')


class ResultDetailLabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResultDetailLabelModel
        fields = ('description', 'score')


class ResultDetailSerializer(serializers.HyperlinkedModelSerializer):
    position = ResultDetailPositionSerializer(read_only=True)
    label = ResultDetailLabelSerializer(many=True, read_only=True)

    class Meta:
        model = ResultDetailModel
        fields = ('position', 'label')


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    module_name = serializers.CharField(source='get_module_name', read_only=True)
    module_result = ResultDetailSerializer(many=True, read_only=True)

    class Meta:
        model = ResultModel
        fields = ('module_name', 'module_result')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = ImageModel
        fields = ('image', 'modules', 'token', 'uploaded_date', 'updated_date', 'results')
        read_only_fields = ('token', 'uploaded_date', 'updated_date', 'results')

