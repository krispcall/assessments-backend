import os
from celery import Celery

# set the default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task.settings')

app = Celery('task')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()