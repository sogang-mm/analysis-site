# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from ModuleManager.serializers import *
from rest_framework import viewsets


class ModulesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModuleModel.objects.all()
    serializer_class = ModuleSerializer

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__contains=name)

        url = self.request.query_params.get('url', None)
        if url is not None:
            queryset = queryset.filter(url__contains=url)

        status = self.request.query_params.get('status', None)
        if status is not None:
            status = 1 if status == 'true' else 0
            queryset = queryset.filter(status__exact=status)

        return queryset


class ModulesGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModuleGroupModel.objects.all()
    serializer_class = ModuleGroupSerializer

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get('name', None)
        if name is not None:
            groups = queryset.filter(name__contains=name)
            detail = queryset.filter(modules__name__contains=name)
            queryset = groups.union(detail)

        return queryset
