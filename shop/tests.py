# import pytest
# from django.urls import reverse
# from rest_framework.test import APIClient
# from shop.models import Shop, Category, Product
#
# @pytest.fixture
# def api_client():
#     return APIClient()
#
# @pytest.mark.django_db
# def test_get_shop(api_client):
#     url = reverse('shop')
#     response = api_client.get(url)
#     assert response.status_code == 200
#     assert 'shop' in response.data
#
# @pytest.mark.django_db
# def test_create_category(api_client):
#     url = reverse('create_category')
#     data = {
#         'name': 'Test Category',
#         'description': 'This is a test category',
#     }
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == 201
#     assert Category.objects.filter(name='Test Category').exists()
#
# @pytest.mark.django_db
# def test_update_product(api_client):
#     product = Product.objects.create(name='Test Product', price=10.0)
#     url = reverse('update_product', kwargs={'pk': product.pk})
#     data = {
#         'name': 'Updated Product',
#         'price': 15.0,
#     }
#     response = api_client.put(url, data, format='json')
#     assert response.status_code == 200
#     assert Product.objects.get(pk=product.pk).name == 'Updated Product'
#
# # Add more test cases to achieve 50% coverage...

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_account(api_client):
    url = reverse('register-account')
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'password': 'password123',
        'company': 'Example Company',
        'position': 'Developer'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['Status'] == True

@pytest.mark.django_db
def test_confirm_account(api_client):
    url = reverse('confirm-account')
    data = {
        'email': 'johndoe@example.com',
        'token': 'example_token'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['Status'] == True

@pytest.mark.django_db
def test_account_details(api_client, user):
    url = reverse('account-details')
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == user.id

@pytest.mark.django_db
def test_login_account(api_client, user):
    url = reverse('login-account')
    data = {
        'email': user.email,
        'password': 'password123'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['Status'] == True

@pytest.mark.django_db
def test_category_view(api_client):
    url = reverse('category-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

@pytest.mark.django_db
def test_shop_view(api_client):
    url = reverse('shop-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0