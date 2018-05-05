# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from rest_framework import exceptions
from ModuleCommunicator import tasks
from ModuleManager.models import *
import json, ast


class ImageModel(models.Model):
    image = models.ImageField()
    token = models.AutoField(primary_key=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modules = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super(ImageModel, self).save(*args, **kwargs)

        module_group_list = self.modules.split(',')
        module_set = ModuleModel.objects.get_queryset()

        for module_group in module_group_list:
            try:
                modules_in_group = ModuleGroupModel.objects.get(name=module_group.strip())
                module_set.union(modules_in_group.modules.all())
            except:
                raise exceptions.ValidationError('Module not found. Please check and send again.')

        module_result = list()

        for module in module_set.all():
            module_result.append(self.results.create(module=module))

        for module in module_result:
            module.get_result()

        super(ImageModel, self).save()


class ResultModel(models.Model):
    result = models.TextField(null=True)
    image = models.ForeignKey(ImageModel, related_name='results', on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleModel)
    task = None

    class Meta:
        unique_together = ('module', 'image')
        ordering = ['module']

    def __unicode__(self):
        return "{0} : {1}".format(self.module.name, self.result)

    def save(self, *args, **kwargs):
        super(ResultModel, self).save(*args, **kwargs)
        self.set_task()
        super(ResultModel, self).save()

    # Celery Delay
    def set_task(self):
        try:
            self.task = tasks.post_image_and_get_result.delay(url=self.module.url, image_path=self.image.image.path)
        except:
            self.task = None

    # Celery Get
    def get_result(self):
        if self.task is not None:
            task_get = self.task.get()
            self.result = ast.literal_eval(task_get)
        else:
            self.result = u"Module Error. Please contact the administrator"
        super(ResultModel, self).save()

