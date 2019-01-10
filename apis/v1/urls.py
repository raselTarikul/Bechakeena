from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', csrf_exempt(RegisterDevice.as_view()), name='device_registration'),
    path('login/', csrf_exempt(Login.as_view()), name='device_login'),
    path('change_pin/', csrf_exempt(ChangePassword.as_view()), name='device_login'),
    path('categories/', csrf_exempt(CategoryList.as_view()), name='category_list'),
    path('categories/<int:pk>/products/', csrf_exempt(ProductListByCategory.as_view()), name='category_list'),
    path('products/', csrf_exempt(ProductList.as_view()), name='products_list'),
    path('create_order/', csrf_exempt(CreateOrder.as_view()), name='create_order'),
    path('orders/', csrf_exempt(GetOrderList.as_view()), name='order_list'),

]
