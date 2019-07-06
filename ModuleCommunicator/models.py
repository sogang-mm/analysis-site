# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.postgres.fields import JSONField
from rest_framework import exceptions
from AnalysisSite.config import DEBUG
from AnalysisSite.config import PROFILE
from ModuleCommunicator.tasks import communicator
from ModuleCommunicator.utils import filename
from ModuleManager.models import *

from Profile.timer import *


class ImageModel(models.Model):
    image = models.ImageField(upload_to=filename.uploaded_date)
    token = models.AutoField(primary_key=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modules = models.TextField(blank=True)
    profile = JSONField(null=True)

    def save(self, *args, **kwargs):
        super(ImageModel, self).save(*args, **kwargs)

        if PROFILE :
            self.profile = {'analysis-site': None, 'analysis-module': None, 'total_time': None}
            total_start = start_time()
            module_set, module_result = self.init_module()

            start = start_time()
            self.create_task(module_set, module_result)
            create_task_time = end_time(start)

            start = start_time()
            self.get_results(module_result)
            get_result_time = end_time(start)
            
            self.profile['analysis-site'] = {
                "create_task_time": create_task_time,
                "get_result_time": get_result_time
            }
            total_end = end_time(total_start)
            self.profile['total_time'] = total_end

        else :
            module_set, module_result = self.init_module()
            self.create_task(module_set, module_result)

            self.get_results(module_result)

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

    def init_module(self):
        return self.get_module(), list()

    def create_task(self, module_set, module_result):
        for module in module_set.all():
            module_result.append(self.results.create(module=module))

    def get_results(self, module_result):
        if PROFILE :
            self.profile['analysis-module'] = []
            for result in module_result:
                module_result = {
                    'module_name' : result.module.name,
                    'module_result' : result.get_result()
                }
                self.profile['analysis-module'].append(module_result)
        else :
            for result in module_result:
                result.get_result()

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
        try:
            if PROFILE:
                self.task, self.model_inference_time, self.result_save_time = communicator(url=self.module.url, image_path=self.image.image.path)
            elif DEBUG:
                self.task = communicator(url=self.module.url, image_path=self.image.image.path)
            else:
                self.task = communicator.delay(url=self.module.url, image_path=self.image.image.path)
        except:
            raise exceptions.ValidationError("Module Set Error. Please contact the administrator")

    # Celery Get
    def get_result(self):
        try:
            if DEBUG:
                self.module_result = self.task
            else:
                self.module_result = self.task.get()
        except:
            raise exceptions.ValidationError("Module Get Error. Please contact the administrator")
        super(ResultModel, self).save()
        if PROFILE :
            return {"model_inference_time": self.model_inference_time, 'result_save_time' : self.result_save_time}

    def get_module_name(self):
        return self.module.name
