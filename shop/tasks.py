from celery import shared_task
# from easy_thumbnails.files import get_thumbnailer
from .models import *

@shared_task
def process_avatar(user_id):
    # Обработка аватара пользователя
    pass

@shared_task
def process_product_image(product_id):
    # Обработка изображения товара
    pass
