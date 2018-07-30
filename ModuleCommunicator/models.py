# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.postgres.fields import JSONField
from rest_framework import exceptions
from ModuleCommunicator.tasks import communicator
from ModuleCommunicator.utils import filename
from ModuleManager.models import *


class ImageModel(models.Model):
    image = models.ImageField(upload_to=filename.uploaded_date)
    token = models.AutoField(primary_key=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modules = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super(ImageModel, self).save(*args, **kwargs)

        module_set = self.get_module()
        module_result = list()

        for module in module_set.all():
            module_result.append(self.results.create(module=module))

        for result in module_result:
            result.get_result()
        super(ImageModel, self).save()

    # Get ModuleModel item from self.modules
    def get_module(self):
        if len(self.modules) == 0:
            return ModuleElementModel.objects.all()

        module_group_list = self.modules.split(',')
        module_set = None

        for module_group in module_group_list:
            try:
                modules_in_group = ModuleGroupModel.objects.get(name=module_group.strip())
            except:
                raise exceptions.ValidationError('Module not found. Please check and send again.')

            if module_set is None:
                module_set = modules_in_group.elements.all()
            else:
                module_set = module_set | modules_in_group.elements.all()

        return module_set.distinct()


class ResultModel(models.Model):
    image = models.ForeignKey(ImageModel, related_name='results', on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleElementModel)
    module_result = JSONField(null=True)

    def save(self, *args, **kwargs):
        super(ResultModel, self).save(*args, **kwargs)
        self.set_task()
        super(ResultModel, self).save()

    # Celery Delay
    def set_task(self):
        self.task = None
        try:
            self.task = communicator.delay(url=self.module.url, image_path=self.image.image.path)
        except:
            raise exceptions.ValidationError("Module Set Error. Please contact the administrator")

    # Celery Get
    def get_result(self):
        try:
            self.module_result = self.task.get()
        except:
            raise exceptions.ValidationError("Module Get Error. Please contact the administrator")
        super(ResultModel, self).save()

    def get_module_name(self):
        return self.module.name
