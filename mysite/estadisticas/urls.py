from django.shortcuts import render
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<examen_id>[0-9]+)/estadis_examen', views.estadis_examen, name="estadis_examen"),
    url(r'^(?P<materia>\w+)/estadis', views.estadis, name='estadis'),
    url(r'^', views.estadistica_view, name='estadisticas'),
]
