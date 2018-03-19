# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from AnalysisModules import tasks
import json


class ModulesModel(models.Model):
    name = models.TextField(unique=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)


class ImageModel(models.Model):
    image = models.ImageField()
    token = models.AutoField(primary_key=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modules = models.TextField()
    result = models.TextField(null=True)

    def save(self, *args, **kwargs):
        super(ImageModel, self).save(*args, **kwargs)
        module_list = self.modules.split(',')

        result_model_list = []
        for module_name in module_list:
            result_model = self.resultmodel_set.create(module_name=module_name)
            result_model_list.append(result_model)

        result_dict = dict()

        for result_model in result_model_list:
            result_model.get_result()
            result_dict[str(result_model.module_name)] = str(result_model.result)

        self.result = json.dumps(result_dict)

        super(ImageModel, self).save()


class ResultModel(models.Model):
    module_name = models.TextField(null=True)
    result = models.TextField(null=True)
    image = models.ForeignKey(ImageModel)

    def save(self, *args, **kwargs):
        super(ResultModel, self).save(*args, **kwargs)

        # Celery Delay
        try:
            url = ModulesModel.objects.get(name=self.module_name).url
            self.task = tasks.post_image_and_get_result.delay(url=url, image_path=self.image.image.path)
        except:
            self.task = None

        super(ResultModel, self).save()

    def get_result(self):
        # Celery Get
        if self.task is not None:
            self.result = self.task.get()
        else:
            self.result = u"Module not found. Please check and send again."

