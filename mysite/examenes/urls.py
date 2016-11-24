from django.shortcuts import render
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<examen_id>[0-9]+)/(?P<pregunta_id>[0-9]+)/nota_reportada', views.nota_reportada, name='nota_reportada'),
    url(r'^(?P<examen_id>[0-9]+)/(?P<pregunta_id>[0-9]+)/reportar', views.reportar, name='reportar'),
    url(r'^(?P<examen_id>[0-9]+)/respuesta', views.respuesta, name='respuesta'),
    url(r'^(?P<examen_id>[0-9]+)/resppreg', views.resppreg, name='resppreg'),
    url(r'^elegirExamen', views.elegirExamen, name='elegirExamen'),
    url(r'^examenencurso', views.examenencurso_view, name='examenencurso'),
    url(r'^select_temas', views.select_temas, name='select_temas'),
    url(r'^examen', views.examen_view, name='examen'),
    url(r'^(?P<examenE_id>[0-9]+)/(?P<temaActual>[0-9]+)/respuestaE', views.respuestaE, name='respuestaE'),
    url(r'^(?P<examenE_id>[0-9]+)/(?P<temaActual>[0-9]+)/respPregErrores', views.respPregErrores, name='respPregErrores'),
    url(r'^(?P<materia>\w+)/encurso', views.examen_encurso, name='encurso'),
    url(r'^selcMateria', views.selcMateria, name='selcMateria'),
    url(r'^selcTemas', views.selcTemas, name='selcTemas'),
]
