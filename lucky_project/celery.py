#celery.py
#Using Celery for asynchronous task processing can significantly improve performance. 
#Celery allows you to run tasks in the background, thus avoiding blocking the main application thread.

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lucky_project.settings')

app = Celery('lucky_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
