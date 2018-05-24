# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from ModuleManager.serializers import *
from rest_framework import viewsets


class ModulesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModuleModel.objects.all()
    serializer_class = ModuleSerializer


class ModulesGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModuleGroupModel.objects.all()
    serializer_class = ModuleGroupSerializer
