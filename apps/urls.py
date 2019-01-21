from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LogIn.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='log_out'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),

    path('categories/', views.CategoryList.as_view(), name='category_list_view'),
    path('categories/new', views.CategoryCreate.as_view(), name='category_create'),
    path('categories/edit/<int:pk>', views.CategoryUpdate.as_view(), name='category_edit'),
    path('categories/delete/<int:pk>', views.CategoryDelet.as_view(), name='category_delete'),

    path('devices/', views.DeviceList.as_view(), name='device_list'),
    path('devices/edit/<int:pk>', views.DeviceUpdate.as_view(), name='device_edit'),
    path('devices/delete/<int:pk>', views.DeviceDelet.as_view(), name='device_delete'),
    path('devices/<int:pk>/reset', views.RestPin.as_view(), name='device_reset_pin'),

    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/new', views.ProductCreate.as_view(), name='product_create'),
    path('products/edit/<int:pk>', views.ProductUpdate.as_view(), name='product_edit'),
    path('products/delete/<int:pk>', views.CategoryDelet.as_view(), name='product_delete'),

    path('orders/', views.OrderList.as_view(), name='order_list_view'),
    path('orders/<int:pk>', views.OrderDetails.as_view(), name='order_details'),
    path('orders/<int:pk>/complete', views.OrderComplete.as_view(), name='order_complete'),
    path('orders/<int:pk>/cancel', views.OrderCancel.as_view(), name='order_cancel'),
]