from celery import Celery

from orders.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


celery_app = Celery('diploma', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery_app.autodiscover_tasks()