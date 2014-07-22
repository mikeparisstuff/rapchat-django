from __future__ import absolute_import

from .rapback_celery import app as celery_app

__all__ = ['celery_app']
