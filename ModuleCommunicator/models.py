# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from rest_framework import exceptions
from ModuleCommunicator.tasks import communicator
from ModuleCommunicator.utils import filename
from ModuleManager.models import *
import ast


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
            return ModuleModel.objects.all()

        module_group_list = self.modules.split(',')
        module_set = None

        for module_group in module_group_list:
            try:
                modules_in_group = ModuleGroupModel.objects.get(name=module_group.strip())
            except:
                raise exceptions.ValidationError('Module not found. Please check and send again.')

            if module_set is None:
                module_set = modules_in_group.modules.all()
            else:
                module_set = module_set | modules_in_group.modules.all()

        return module_set


class ResultModel(models.Model):
    image = models.ForeignKey(ImageModel, related_name='results', on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleModel)

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
            raise exceptions.ValidationError("Module Error. Please contact the administrator")

    # Celery Get
    def get_result(self):
        try:
            task_get = ast.literal_eval(self.task.get())
            for result in task_get:
                self.module_result.create(position=result[0], values=result[1])
        except:
            raise exceptions.ValidationError("Module Error. Please contact the administrator")

    def get_module_name(self):
        return self.module.name


class ResultDetailModel(models.Model):
    result_model = models.ForeignKey(ResultModel, related_name='module_result', on_delete=models.CASCADE)
    position = models.TextField()
    values = models.TextField()

    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    w = models.FloatField(null=True)
    h = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if not (isinstance(self.position, list) and isinstance(self.values, dict)):
            raise exceptions.ValidationError("Module return value Error. Please contact the administrator")
        super(ResultDetailModel, self).save(*args, **kwargs)
        self.x, self.y, self.w, self.h = self.position
        for item in self.values.items():
            self.prediction.create(label=item[0], score=float(item[1]))
        super(ResultDetailModel, self).save()


class ResultDetailListModel(models.Model):
    result_detail_model = models.ForeignKey(ResultDetailModel, related_name='prediction', on_delete=models.CASCADE)
    label = models.TextField(null=True, unique=False)
    score = models.FloatField(null=True, unique=False)

    class Meta:
        ordering = ['-score']
