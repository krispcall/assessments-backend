import os
import django
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmanagementsystem.settings')
django.setup()

app = Celery('bookmanagementsystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()