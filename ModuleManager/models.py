# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from rest_framework import exceptions
import requests


class ModuleElementModel(models.Model):
    name = models.TextField(unique=True)
    url = models.URLField()
    content = models.TextField(blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(ModuleElementModel, self).save(*args, **kwargs)
        try:
            response = requests.get(self.url)
            self.status = response.ok
        except:
            raise exceptions.ValidationError('Cannot access URL. Check module URL.')

        self.group.update_or_create(name=self.name, content=self.content)
        super(ModuleElementModel, self).save()


class ModuleGroupModel(models.Model):
    name = models.TextField(unique=True)
    modules = models.ManyToManyField(ModuleElementModel, related_name='group')
    content = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
