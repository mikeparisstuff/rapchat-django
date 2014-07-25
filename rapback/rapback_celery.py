from __future__ import absolute_import
from django.conf import settings
from celery import Celery
import redis

settings.configure()

app = Celery('rapback.celery',
        broker='sqs://sqs.us-east-1.amazonaws.com/487142144782/rapback-celery-broker//'
        )

app.conf.update(
        CELERY_TASK_SERIALIZER = 'json',
        CELERY_RESULT_SERIALIZER = 'json',
        CELERY_ENABLE_UTC = True
        )

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()
