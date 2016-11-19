from django.shortcuts import render
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<examen_id>[0-9]+)/(?P<pregunta_id>[0-9]+)/reportar', views.reportar, name='reportar'),
    url(r'^(?P<examen_id>[0-9]+)/respuesta', views.respuesta, name='respuesta'),
    url(r'^(?P<examen_id>[0-9]+)/resppreg', views.resppreg, name='resppreg'),
    url(r'^elegirExamen', views.elegirExamen, name='elegirExamen'),
    url(r'^examen', views.examen_view, name='examen'),
    url(r'^examenencurso', views.examenencurso_view, name='examenencurso'),
    url(r'^selcMateria', views.selcMateria, name='selcMateria'),
    url(r'^selcTemas', views.selcTemas, name='selcTemas'),
    url(r'^encurso', views.examen_encurso, name='encurso'),
]
