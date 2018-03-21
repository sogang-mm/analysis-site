from django.forms import widgets
from rest_framework import serializers
from ModuleCommunicator.models import *


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('image', 'modules', 'token', 'uploaded_date', 'updated_date', 'result')
        read_only_fields = ('token', 'uploaded_date', 'updated_date', 'result')


# class ResultSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ResultModel
#         fields = ('result')
#         read_only_fields = ('result')