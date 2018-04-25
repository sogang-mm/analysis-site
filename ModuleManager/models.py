# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from rest_framework import exceptions
import requests


class ModuleModel(models.Model):
    name = models.TextField(unique=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(ModuleModel, self).save(*args, **kwargs)
        response = requests.get(self.url)
        if response.ok is False:
            raise exceptions.ValidationError('Cannot access URL. Check module URL.')
        self.modulegroupmodel_set.create(name=self.name, modules_list=self.name, description=self.description)
        super(ModuleModel, self).save()


class ModuleGroupModel(models.Model):
    name = models.TextField(unique=True)
    modules_list = models.TextField(blank=True)
    modules = models.ManyToManyField(ModuleModel)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        modules_name_list = self.modules_list.split(',')

        modules_list = list()
        for module_name in modules_name_list:
            modules = ModuleModel.objects.filter(name=module_name.strip())
            if modules.count() == 0:
                raise exceptions.ValidationError('Module not found. Check module name.')
            modules_list.append(modules.first())

        super(ModuleGroupModel, self).save(*args, **kwargs)

        for modules in modules_list:
            self.modules.add(modules)

        super(ModuleGroupModel, self).save()
