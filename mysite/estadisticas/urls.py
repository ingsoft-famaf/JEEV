from django.shortcuts import render
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^', views.estadistica_view, name='estadisticas'),
    #url(r'^general', views.general, name='general'),
]
