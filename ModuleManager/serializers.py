from django.forms import widgets
from rest_framework import serializers
from ModuleManager.models import *


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ModuleModel
        fields = ('name', 'url', 'content', 'status')


class ModuleGroupSerializer(serializers.HyperlinkedModelSerializer):
    modules = ModuleSerializer(many=True)

    class Meta:
        model = ModuleGroupModel
        fields = ('name', 'content', 'modules')