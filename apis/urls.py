from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

urlpatterns = [
    url(r'^v1/', include('apis.v1.urls')),

]
