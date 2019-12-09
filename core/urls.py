from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('registration/', views.RegisterFormView.as_view(), name='registration'),
    path('ajax/', views.index.request_ajax, name='request_ajax'),
    path('', views.index.IndexView.as_view(), name='index'),
]