from django.shortcuts import render
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^examenencurso', views.examenencurso_view, name='examenencurso'),
    url(r'^examen', views.examen_view, name='examen'),
]
