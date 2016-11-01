from django.shortcuts import render
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'cargarmateria/', views.cargarmateria, name='cargarmateria'),
    url(r'cargartema/', views.cargartema, name='cargartema'),
]
