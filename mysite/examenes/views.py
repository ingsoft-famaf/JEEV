# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from questions.models import Question, Answer
from .models import Exam, PregResp, TemaE
from materias.models import Materia, Tema
import questions.models
import random
from django.http import HttpResponse
import json
from itertools import chain


def filter_query(realquery, querytofilt):
    for q in querytofilt:
        for q2 in realquery:
            if q.question.id == q2.id:
                realquery = realquery.exclude(id=q2.id)
    return realquery


def filter_pregunta(result, queryresp):
    lista = []
    for q in queryresp:
        contador = 0
        for r in result:
            print ("esto es q dentro del for %s" % q.question.text_preg)
            if q.question.id == r.id:
                lista = result.pop(contador)
                print ("esto es el eliminado %s" % lista)
            contador += 1
    return result

def guardar_tema(Exam, tema):
    modelTema=TemaE(tema_fk=Exam, nombre_tema=tema)
    modelTema.save()


def select_temas(request):
    """
    Input : HttpRequest
    Output : redirige a un html
    Esta función muestra los temas de una materia preseleccionada.
    """
    mat = request.GET['materia']
    materia = get_object_or_404(Materia, nombre_materia=mat)
    temas = Tema.objects.filter(temas=materia)
    temas = [tema.nombre_tema for tema in temas]
    return HttpResponse(json.dumps(temas), content_type="application/json")


def examen_view(request):
    """
        Esta funcion muestra las opciones para la configuracion del examen.
        :param request: HttpRequest
        :type: Http
        :return: redirige a un html pasandole dos query
    """
    return render(request, 'examenes/examen.html',
                  {'list_materias': Question.objects.values_list('nombre_materia', flat=True).distinct(),
                   'list_temas': Question.objects.values_list('nombre_tema', flat=True).distinct()})


def examenencurso_view(request):
    """
    Esta funcion recoge la configuracion del usuario y le indica al usuario
    que la configuracion se realizo correctamente.
    :param request: HttpRequest
    :return: redirige a un html pasandole una query
    """
    if request.POST['cantidad'] == "":
        return render(request, 'examenes/vacio.html')
    materia = request.POST['materias']
    tema = request.POST.getlist('tema')
    #import pdb
    #pdb.set_trace()
    cant_temas = len(tema)
    cantidad = request.POST['cantidad']
    tiempo = request.POST['tiempo']
    tema_vacio = False
    temas_vacios = []
    cantidad_preg_bd = 0
    for x in xrange(cant_temas):
        query = Question.objects.filter(nombre_materia=materia).filter(nombre_tema=tema[x])
        if query.count() == 0:
            tema_vacio = True
            temas_vacios.append(tema[x])
            #pasar a examenen curso y botones en html
        cantidad_preg_bd += query.count()
    if int(cantidad) > cantidad_preg_bd:
        return render(request, 'examenes/validarCant.html', {'cantidad': cantidad_preg_bd})
    examen = Exam(nombre_materia=materia, cantidad_preg=cantidad, tiempo_preg=tiempo)
    examen.save()
    for i in range(cant_temas):
        nombre_tema = str(tema[i])
        guardar_tema(examen, nombre_tema)
    return render(request, 'examenes/examenencurso.html', {'examen': examen})


def resppreg(request, examen_id):
    """
    Esta función muestra una pregunta con sus respuestas para que el usuario
    haga la elección de un de ellas.
    :Param  request: HttpRequest
    :Param examen_id: id del examen
    :return: redirige a un html pasándole dos query
    """
    examen = get_object_or_404(Exam, pk=examen_id)
    temas = TemaE.objects.filter(tema_fk=examen)   
    materia = str(examen.nombre_materia)
    randomm = []
    query_vacia = []
    query = []
    cantidad_temas = temas.count()
    if examen.pregunta_actual == examen.cantidad_preg:
        nota = examen.preguntas_correctas
        nota1 = examen.cantidad_preg
        examen.porcentaje = ((nota * 100) / nota1)
        examen.save()
        return render(request, 'examenes/finalizo.html', {'examen': examen})
    if cantidad_temas == 1:
        result = Question.objects.filter(nombre_tema=temas[0]).filter(nombre_materia=materia).filter(reportada=False)
        queryresp = PregResp.objects.filter(examen=examen)
        query = filter_query(result, queryresp)
        randomm = random.sample(query, 1)
        pregunta = randomm[0]
    else:
        for x in xrange(cantidad_temas):
            query.append(Question.objects.filter(nombre_tema=temas[x]).filter(nombre_materia=materia).filter(reportada=False))
            result = list(chain(query_vacia, query[x]))
            query_vacia = result

        #print ("lista de chain %s" % result)
        queryresp = PregResp.objects.filter(examen=examen)
        #print result
        #print pregunta
        query = filter_pregunta(result, queryresp)
        print query
        randomm = random.sample(query, 1)
        pregunta = randomm[0]
    PregResp.objects.create(examen=examen, question=pregunta)
    return render(request, 'examenes/resppreg.html',
                  {'pregunta': pregunta, 'examen': examen})


def respuesta(request, examen_id):
    """
    Esta función recoge la respuesta seleccionada y le indica al usuario si
    es correcta o no. Si no responde en el tiempo predeterminado le indica que
    la respuesta es incorrecta.
    :Param request: HttpRequest
    :Param examen_id: id del examen
    :return: redirige a un html pasandole una query
    """
    if request.method == 'POST':
        respuesta_id = request.POST['respuesta']
        examen = get_object_or_404(Exam, pk=examen_id)
        examen.pregunta_actual += 1
        examen.save()
        respuesta = get_object_or_404(Answer, pk=respuesta_id)
        if respuesta.es_correcta:
            examen.preguntas_correctas += 1
        else:
            examen.preguntas_incorrectas += 1
        examen.save()
        return render(request, 'examenes/respuesta.html',
                      {'respuesta': respuesta, 'examen': examen})
    examen = get_object_or_404(Exam, pk=examen_id)
    examen.pregunta_actual += 1
    examen.preguntas_incorrectas += 1
    examen.save()
    return render(request, 'examenes/respuesta.html', {'examen': examen})


def nota_reportada(request, examen_id, pregunta_id):
    return render(request, 'examenes/nota_reportada.html',
                  {'pregunta': pregunta_id, 'examen': examen_id})


def reportar(request, examen_id, pregunta_id):
    """
    Esta funcipn le indica al usuario que la pregunta fue reportada.
    :Param request: HttpRequest
    :Param examen_id: id del examen
    :Param pregunta_id: id de la pregunta
    :retun: redirige a un html pasandole dos query
    """
    if request.method == "POST":
        nota = request.POST['nota']
        if nota == "":
            return render(request, 'examenes/nota_reportada.html',
                          {'pregunta': pregunta_id, 'examen': examen_id})
        examen = get_object_or_404(Exam, pk=examen_id)
        pregunta = get_object_or_404(Question, pk=pregunta_id)
        pregunta.reportada = True
        pregunta.nota_reporte = nota
        pregunta.save()
        examen.cantidad_preg -= 1
        examen.save()
        return render(request, 'examenes/respuesta.html',
                      {'pregunta': pregunta, 'examen': examen})
    examen = get_object_or_404(Exam, pk=examen_id)
    pregunta = get_object_or_404(Question, pk=pregunta_id)
    return render(request, 'examenes/resppreg.html',
                  {'pregunta': pregunta, 'examen': examen})
