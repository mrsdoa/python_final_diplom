from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from requests import get
from yaml import load as load_yaml, Loader
from orders.celery import celery_app
from shop.models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, ConfirmEmailToken

#письмо с токеном для сброса пароля
@celery_app.task()
def password_reset_token_created_task(sender, instance, reset_password_token, **kwargs):

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {reset_password_token.user}",
        # message:
        reset_password_token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.send()


@celery_app.task()
def new_user_registered_task(user_id, **kwargs):
    # письмо подтверждение электронной почты
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {token.user.email}",
        # message:
        token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [token.user.email]
    )
    msg.send()

# письмо об изменении статуса заказа
@celery_app.task()
def new_order_task(user_id, **kwargs):

    user = User.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Обновление статуса заказа",
        # message:
        'Заказ сформирован',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()

# импорт прайса от поставщика
@celery_app.task()
def do_import_task(partner_id, url):

    stream = get(url).content

    data = load_yaml(stream, Loader=Loader)
    # print(data)

    shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=partner_id)

    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()

    ProductInfo.objects.filter(shop_id=shop.id).delete()
    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

        product_info = ProductInfo.objects.create(product_id=product.id,
                                                  external_id=item['id'],
                                                  model=item['model'],
                                                  price=item['price'],
                                                  price_rrc=item['price_rrc'],
                                                  quantity=item['quantity'],
                                                  shop_id=shop.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_info_id=product_info.id,
                                            parameter_id=parameter_object.id,
                                            value=value)