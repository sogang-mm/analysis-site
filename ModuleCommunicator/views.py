# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from ModuleCommunicator.models import *
from ModuleCommunicator.serializers import *
from rest_framework import viewsets, generics


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer


class ModulesViewSet(viewsets.ModelViewSet):
# class ModulesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModulesModel.objects.all()
    serializer_class = ModulesSerializer


class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ResultModel.objects.all()
    serializer_class = ResultSerializer

