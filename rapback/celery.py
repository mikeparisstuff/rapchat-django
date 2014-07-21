from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rapback.settings')

app = Celery('rapback-celery',
             broker='sqs://sqs.us-west-2.amazonaws.com/487142144782/rapback-rapsession-queue//')

app.config_from_object('djagno.conf:settings')
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)

app.conf.update(
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_ENABLE_UTC = True
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))