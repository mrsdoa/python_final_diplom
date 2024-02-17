# from django.contrib import admin
from django.urls import path, include
# from baton.autodiscover import admin as baton_admin

urlpatterns = [
    # path('admin/', baton_admin.site.urls),
    path('api/v1/', include('shop.urls', namespace='shop')),
    path('accounts/', include('allauth.urls')),
]
