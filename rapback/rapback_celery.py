from __future__ import absolute_import
import os
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

@app.task(name='rapback.rapback_celery.add')
def add(x, y):
    print 'Working on add task'
    return x+y

@app.task(name='rapback.rapback_celery.increment_page_hit_count')
def increment_page_hit_count():
    print 'Incrementing page hit count'
    r = redis.StrictRedis('ec2-54-210-10-162.compute-1.amazonaws.com', port=6379, db=0)
    r.incr('page_hit_count')

if __name__ == '__main__':
    app.start()
