# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from AnalysisSite.config import VIEWSET_NUMBER
from ModuleCommunicator.serializers import *
from rest_framework import viewsets


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        view_queryset = self.queryset.order_by('-token')
        if view_queryset.count() < VIEWSET_NUMBER:
            return view_queryset
        return view_queryset[:VIEWSET_NUMBER].reverse()


# class ResultViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = ResultModel.objects.all()
#     serializer_class = ResultSerializer
