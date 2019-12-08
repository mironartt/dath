from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import index

urlpatterns = [
    path('ajax/', index.request_ajax, name='request_ajax'),
    path('', index.IndexView.as_view(), name='index'),
]