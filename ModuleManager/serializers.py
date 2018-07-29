from django.forms import widgets
from rest_framework import serializers
from ModuleManager.models import *


class ModuleElementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ModuleElementModel
        fields = ('name', 'url', 'content', 'status')


class ModuleGroupSerializer(serializers.HyperlinkedModelSerializer):
    modules = ModuleElementSerializer(many=True)

    class Meta:
        model = ModuleGroupModel
        fields = ('name', 'content', 'modules')