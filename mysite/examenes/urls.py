from django.shortcuts import render
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<examen_id>[0-9]+)/resppreg', views.resppreg, name='resppreg'),
    url(r'^examenencurso', views.examenencurso_view, name='examenencurso'),
    url(r'^examen', views.materia_tema_exist, name='exist'),
]
