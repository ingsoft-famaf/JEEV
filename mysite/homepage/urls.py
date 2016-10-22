from django.shortcuts import render
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.homepage, name='profile'),
    #url(r'^$', views.index, name='index'),
]
