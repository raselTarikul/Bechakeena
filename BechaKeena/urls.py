"""BechaKeena URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings

schema_view = get_swagger_view(title='Bechakena API v1')


urlpatterns = [
    path('rest-auth', include('rest_framework.urls')),
    path('swagger/', schema_view),
    path('admin/', admin.site.urls),
    path('apps/', include('apps.urls')),
    path('apis/', include('apis.urls')),
   url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]

]

