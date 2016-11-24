# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from examenes.models import Exam, TemaE
from materias.models import Materia
from django.db.models import Avg, Sum, FloatField
from graphos.sources.model import ModelDataSource
from graphos.renderers import flot


def estadis(request, materia):
    """
    Esta funcion devuelve las estadisticas generales de la materia seleccionada.
    :param request: HttpRequest
    :param materia: String
    :type: POST
    :return:html
    """
    lista_examenes = Exam.objects.filter(nombre_materia=materia)
    cant_preguntas = lista_examenes.aggregate(Sum('cantidad_preg'))
    preg_correctas = lista_examenes.aggregate(Sum('preguntas_correctas'))
    preg_incorrectas = lista_examenes.aggregate(Sum('preguntas_incorrectas'))
    materia = get_object_or_404(Materia, nombre_materia=materia)
    promedio = materia.promedio
    data_source = ModelDataSource(queryset=lista_examenes, fields=['pk', 'porcentaje'])
    chart = flot.LineChart(data_source, height=300, width=500)
    return render(request, 'estadisticas/general.html',
                  {'lista_examenes': lista_examenes, 'cant_preguntas': cant_preguntas,
                   'preg_correctas': preg_correctas, 'preg_incorrectas': preg_incorrectas,
                   'materia': materia, 'promedio': promedio, 'chart': chart})


def estadistica_view(request):
    """
    Esta funcion genera los promedios de cada materia, según los examenes realizados por el usuario.
    :param request: HttpRequest
    :type: Http
    :return: redirige a un html pasándole la lista de las materias
    """
    lista_materias = Exam.objects.values_list('nombre_materia', flat=True).distinct()
    materias = []
    for x in xrange(lista_materias.count()):
        lista_examenes = Exam.objects.filter(nombre_materia=lista_materias[x])
        promedio = lista_examenes.aggregate(Sum('preguntas_correctas'))
        cant_preguntas = lista_examenes.aggregate(Sum('cantidad_preg'))
        suma = float(promedio['preguntas_correctas__sum'])
        cantidad = float(cant_preguntas['cantidad_preg__sum'])
        promedio = float(suma / cantidad)
        materia = get_object_or_404(Materia, nombre_materia=lista_materias[x])
        materia.promedio = promedio * 10
        materia.save()
        materias.insert(x, Materia.objects.get(nombre_materia=lista_materias[x]))
    return render(request, 'estadisticas/estadis.html', {'materias': materias})


def estadis_examen(request, examen_id):
    """ opera la estadisticas y devuelve un resultado
      :param estadis_exam: pedido de html , el id del examen realizado.
      :return: html"""
    examen = get_object_or_404(Exam, pk=examen_id)
    temas = TemaE.objects.filter(tema_fk=examen)
    return render(request, 'estadisticas/estadisExamen.html',
                  {'examen': examen, 'temas': temas})
