from django.shortcuts import render
from django.conf.urls import url
from allauth.account.views import SignupView, LogoutView

from . import views

urlpatterns = [
    url(r'superuser', views.superuser_view, name='superuser'),
    url(r'^', views.homepage, name='homepage'),
]
