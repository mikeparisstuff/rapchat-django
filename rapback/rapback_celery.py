from __future__ import absolute_import
import os
from django.conf import settings
from celery import Celery

settings.configure()

app = Celery('rapback.celery',
        broker='sqs://sqs.us-west-2.amazonaws.com/487142144782/rapback-rapsession-queue//'
        )

app.conf.update(
        CELERY_TASK_SERIALIZER = 'json',
        CELERY_RESULT_SERIALIZER = 'json',
        CELERY_ENABLE_UTC = True
        )

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(name='rapback.rapback_celery.add')
def add(x, y):
    print 'Working on add task'
    return x+y

if __name__ == '__main__':
    app.start()
