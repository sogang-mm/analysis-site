#!/bin/bash
dockerize -wait tcp://postgres:5432 -timeout 20s
sh run_migration.sh
python -c "import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'AnalysisSite.settings'
import django
django.setup()
from django.contrib.auth.management.commands.createsuperuser import get_user_model
if not get_user_model().objects.filter(username='$DJANGO_SUPERUSER_USERNAME'): 
    get_user_model()._default_manager.db_manager().create_superuser(username='$DJANGO_SUPERUSER_USERNAME', email='$DJANGO_SUPERUSER_EMAIL', password='$DJANGO_SUPERUSER_PASSWORD')"
sh start_server.sh
/bin/bash
