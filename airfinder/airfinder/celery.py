from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airfinder.settings')

app = Celery('airfinder')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    'check_price_updates_every_8_hours': {
        'task': 'base.tasks.check_price_updates',
        'schedule': crontab(hour='*/8'),
    },
}
