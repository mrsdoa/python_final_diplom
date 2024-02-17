from celery import Celery

from orders.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


celery_app = Celery('orders', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
