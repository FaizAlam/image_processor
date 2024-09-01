from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_processor.settings')

app = Celery('image_processor')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'amqps://snenqklb:Xa7hAW0sYagTD3xubp06LRLhfxbwYtIz@shrimp.rmq.cloudamqp.com/snenqklb'

app.autodiscover_tasks()
