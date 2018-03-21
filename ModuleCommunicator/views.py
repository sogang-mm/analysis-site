# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from ModuleCommunicator.serializers import *
from rest_framework import viewsets


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer


# class ResultViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = ResultModel.objects.all()
#     serializer_class = ResultSerializer
