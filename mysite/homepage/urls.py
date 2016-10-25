from django.shortcuts import render
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'superuser', views.superuser_view, name='superuser'),
    url(r'index', views.index_view, name='index'),
    url(r'$', views.homepage, name='profile'),
]



    #url(r'^$', views.index, name='index'),
#    url(r'^$', views.DetailView.as_view(), name='detail'),

