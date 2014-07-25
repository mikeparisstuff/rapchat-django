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


@app.task(name='rapback.tasks.add')
def add(x, y):
    print 'Working on add task'
    return x+y

@app.task(name='rapback.tasks.increment_page_hit_count')
def increment_page_hit_count():
    print 'Incrementing page hit count'
    r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    r.incr('page_hit_count')

@app.task(name='rapback.tasks.add_to_feed')
def add_session_to_feed(user_id, session_id):
    r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    key = 'feed:user:{}'.format(user_id)
    with r.pipeline() as pipe:
        while 1:
            try:
                pipe.watch(key)
                val, highest_score = pipe.zrevrange(key, 0, 0, True)[0]
                next_score = int(highest_score) + 1
                pipe.multi()
                pipe.zadd(key, session_id, next_score)
                pipe.execute()
                break
            except IndexError:
                # There are currently no items in this users feed so add one
                r.zadd(key, session_id, 1)
                break
            except redis.WatchError:
                continue




if __name__ == '__main__':
    app.start()
