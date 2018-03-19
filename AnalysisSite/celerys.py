import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AnalysisSite.settings')

app = Celery('AnalysisSite')
app.conf.update(
    broker_url='amqp://localhost',
    result_backend='amqp://localhost',
)
app.autodiscover_tasks()
