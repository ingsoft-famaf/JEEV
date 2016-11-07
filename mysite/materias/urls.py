# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'cargarm', views.cargarm, name='cargarm'),
    #url(r'cargarmateria/', views.cargar_materia, name='cargar_materia'),
    url(r'cargart', views.cargart, name='cargart'),
    #url(r'cargartema/', views.cargartema, name='cargartema'),
    url(r'obtener_tema_materia', views.obtener_tema_materia, name='obtener_tema_materia'),
]
