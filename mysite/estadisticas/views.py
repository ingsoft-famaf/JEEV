from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from examenes.models import Exam
from materias.models import Materia
from django.db.models import Avg, Sum, FloatField
from graphos.sources.model import ModelDataSource
from graphos.renderers import flot


def estadis(request, materia):
    lista_examenes = Exam.objects.filter(nombre_materia=materia)
    data_source = ModelDataSource(queryset=lista_examenes, fields=['pk', 'porcentaje'])
    chart = flot.LineChart(data_source, height=300, width=500)
    cant_preguntas = lista_examenes.aggregate(Sum('cantidad_preg'))
    preg_correctas = lista_examenes.aggregate(Sum('preguntas_correctas'))
    preg_incorrectas = lista_examenes.aggregate(Sum('preguntas_incorrectas'))
    promedio = lista_examenes.aggregate(Avg('preguntas_correctas'))
    promedio= (promedio['preguntas_correctas__avg'])*10
    return render(request, 'estadisticas/general.html',
                  {'lista_examenes': lista_examenes, 'cant_preguntas': cant_preguntas,
                   'preg_correctas':preg_correctas, 'preg_incorrectas': preg_incorrectas,
                   'materia': materia, 'promedio': promedio, 'chart':chart})


def estadistica_view(request):
    """Guarda la estadisticas y reedirije a un html
    :param estadistica_view: pedido de html
    :type: GET  o POST
    :return:html"""
    lista_materias = Exam.objects.values_list(
                        'nombre_materia', flat=True).distinct()
    materias = []
    for x in xrange(lista_materias.count()):
        lista_examenes = Exam.objects.filter(nombre_materia=lista_materias[x])
        promedio = lista_examenes.aggregate(Avg('preguntas_correctas'))
        materia = get_object_or_404(Materia, nombre_materia=lista_materias[x])
        materia.promedio = (promedio['preguntas_correctas__avg'])*10
        materia.save()
        materias.insert(x,Materia.objects.get(nombre_materia=lista_materias[x]))
    #print materias
    return render(request, 'estadisticas/estadis.html', {'materias': materias})


def estadis_examen(request, examen_id):
    """ opera la estadisticas y devuelve un resultado
      :param estadis_exam: pedido de html , el id del examen realizado.
      :return: html"""
    examen = get_object_or_404(Exam, pk=examen_id)
    return render(request, 'estadisticas/estadisExamen.html',
                  {'examen': examen})
