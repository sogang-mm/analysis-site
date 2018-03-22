# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from ModuleCommunicator import tasks
from ModuleManager.models import *
import json


class ImageModel(models.Model):
    image = models.ImageField()
    token = models.AutoField(primary_key=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modules = models.TextField()
    result = models.TextField(null=True)

    def save(self, *args, **kwargs):
        super(ImageModel, self).save(*args, **kwargs)
        module_group_list = self.modules.split(',')

        result_model_list = []
        for module_group_name in module_group_list:
            try:
                module_group = ModuleGroupModel.objects.get(name=module_group_name.strip())
            except:
                self.result = u"Module not found. Please check and send again."
                super(ImageModel, self).save()
                return

            for modules in module_group.modules.all():
                result_model = self.resultmodel_set.create(modules=modules)
                result_model_list.append(result_model)

        result_dict = dict()
        for result_model in result_model_list:
            result_model.get_result()
            result_dict[str(result_model.modules.name)] = str(result_model.result)

        self.result = json.dumps(result_dict)

        super(ImageModel, self).save()


class ResultModel(models.Model):
    result = models.TextField(null=True)
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
    modules = models.ForeignKey(ModuleModel)

    def save(self, *args, **kwargs):
        super(ResultModel, self).save(*args, **kwargs)
        # Celery Delay
        try:
            self.task = tasks.post_image_and_get_result.delay(url=self.modules.url, image_path=self.image.image.path)
        except:
            self.task = None
        super(ResultModel, self).save()

    def get_result(self):
        # Celery Get
        if self.task is not None:
            self.result = self.task.get()
        else:
            self.result = u"Module Error. Please contact the administrator"
