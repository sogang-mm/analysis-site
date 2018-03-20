from django.forms import widgets
from rest_framework import serializers
from ModuleManager.models import *


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ModuleModel
        fields = ('name', 'url', 'description', 'status')


class ModuleGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ModuleGroupModel
        fields = ('name', 'description', 'modules_list')