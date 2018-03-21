import os
from celery import Celery
from AnalysisSite import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AnalysisSite.settings')

app = Celery('AnalysisSite')
app.conf.update(
    broker_url='amqp://localhost',
    result_backend='amqp://localhost',
    worker_autoscaler='{0},{1}'.format(config.WORKER_MAX_SCALER, config.WORKER_MIN_SCALER),
    worker_concurrency='{0}'.format(config.WORKER_CONCURRENCY),
)
app.autodiscover_tasks()
