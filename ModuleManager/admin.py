# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from ModuleManager import models


admin.site.register(models.ModuleModel)