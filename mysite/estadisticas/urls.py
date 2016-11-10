from django.shortcuts import render
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<materia>\w+)/grafico', views.grafico, name="grafico"),
    url(r'^(?P<examen_id>[0-9]+)/estadis_examen', views.estadis_examen, name="estadis_examen"),
    url(r'^', views.estadistica_view, name='estadisticas'),
    #url(r'^general', views.general, name='general'),
]
