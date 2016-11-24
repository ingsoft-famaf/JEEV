# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from questions.models import Question, Answer
from .models import Exam, PregResp, TemaE
import random
from materias.models import Materia, Tema
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
            if q.question.id == r.id:
                lista = result.pop(contador)
            contador += 1
    return result


def guardar_tema(Exam, tema):
    modelTema = TemaE(tema_fk=Exam, nombre_tema=tema)
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


def elegirExamen(request):
    """
    Input: HttpRequest
    Output: redirige a un html pasándole dos query
    Esta función muestra las opciones de algoritmos para el examen.
    """
    return render(request, 'examenes/elegirExamen.html')


""" Algoritmo basado en errores"""


def selcMateria(request):
    """
    Input: HttpRequest
    Output: redirige a un html pasándole dos query
    Esta función muestra las opciones de materias para la configuración del examen
    para el algoritmo basado en errores.
    """
    query = Question.objects.all()
    count = query.count()
    print count
    if count == 0:
        return render(request, 'examenes/preguntasCero.html')
    else:
        query = Materia.objects.values_list('nombre_materia', flat=True).distinct()
        return render(request, 'examenes/selcMateria.html',
                      {'list_materias': Materia.objects.values_list('nombre_materia', flat=True).distinct()})


def selcTemas(request):
    """
    Input: HttpRequest
    Output: redirige a un html pasándole dos query
    Esta función muestra las opciones de temas para la configuración del examen
    para el algoritmo basado en errores.
    """
    materia = request.POST['materias']
    list_temas = Tema.objects.values_list('nombre_tema', flat=True).filter(temas__nombre_materia=materia)
    return render(request, 'examenes/selcTemas.html', {'list_temas': list_temas, 'materia': materia})


def examen_encurso(request, materia):

    if request.POST['cantidad'] == "":
        return render(request, 'examenes/datosIncorrectos.html')
    cantidad = request.POST['cantidad']
    tiempo = request.POST['tiempo']
    tema = request.POST.getlist('tema')
    tema_vacio = False
    temas_vacios = []
    cantidad_preg_bd = 0
    cant_temas = len(tema)
    for x in xrange(cant_temas):
        query = Question.objects.filter(nombre_materia=materia).filter(nombre_tema=tema[x])
        if query.count() == 0:
            tema_vacio = True
            temas_vacios.append(tema[x])
        cantidad_preg_bd += query.count()
    if int(cantidad) > cantidad_preg_bd:
        return render(request, 'examenes/validarCant.html', {'cantidad': cantidad_preg_bd})
    examenE = Exam(nombre_materia=materia, cantidad_preg=cantidad, tiempo_preg=tiempo)
    examenE.save()
    for i in range(cant_temas):
        nombreTema = str(tema[i])
        temas = guardar_tema(examenE, nombreTema)
    temaActual = 0
    return render(request, 'examenes/encurso.html',
                  {'examenE': examenE, 'temaActual': temaActual, 'tema_v': tema_vacio, 'temas_v': temas_vacios})


def respPregErrores(request, examenE_id, temaActual):
    """
    Input: HttpRequest y id del examen
    Output: redirige a un html pasándole dos query
    Esta función muestra una pregunta con sus respuestas para que el usuario
    haga la elección de un de ellas.
    """
    temaActual = int(temaActual)
    examen = get_object_or_404(Exam, pk=examenE_id)
    materia = examen.nombre_materia
    temas = TemaE.objects.filter(tema_fk=examen)
    randomm = []
    cantidad_temas = temas.count()
    if examen.pregunta_actual == examen.cantidad_preg:
        nota = examen.preguntas_correctas
        nota1 = examen.cantidad_preg
        if nota1 == 0:
            examen.porcentaje = 0
            examen.save()
        else:
            examen.porcentaje = ((nota * 100) / nota1)
            examen.save()
        return render(request, 'examenes/finalizo.html', {'examen': examen})
    if cantidad_temas == 1:
        nTema = temas[0]
        preguntas = Question.objects.filter(nombre_tema=nTema).filter(nombre_materia=materia).filter(reportada=False)
    else:
        preguntas = Question.objects.filter(nombre_tema=temas[temaActual]).filter(nombre_materia=materia).filter(reportada=False)
    queryresp = PregResp.objects.filter(examen=examen)
    query = filter_query(preguntas, queryresp)
    cant_query = query.count()
    if cant_query == 0:
        if temaActual == (cantidad_temas - 1):
            temaActual = 0
            for i in range(cantidad_temas):
                preguntas = Question.objects.filter(nombre_tema=temas[temaActual]).filter(nombre_materia=materia).filter(reportada=False)
                query = filter_query(preguntas, queryresp)
                query_count = query.count()
                if query_count == 0:
                    temaActual += 1
                else:
                    break
        else:
            temaActual += 1
        preguntas = Question.objects.filter(nombre_tema=temas[temaActual]).filter(nombre_materia=materia).filter(reportada=False)
        query = filter_query(preguntas, queryresp)
    randomm = random.sample(query, 1)
    pregunta = randomm[0]
    PregResp.objects.create(examen=examen, question=pregunta)
    return render(request, 'examenes/respPregErrores.html',
                  {'pregunta': pregunta, 'examenE': examen, 'temaActual': temaActual})


def respuestaE(request, examenE_id, temaActual):
    """
    Input: HttpRequest y id del examen
    Output: redirige a un html pasándole una query
    Esta función recoge la respuesta seleccionada y le indica al usuario si
    es correcta o no. Si no responde en el tiempo predeterminado le indica que
    la respuesta es incorrecta.
    """

    if request.method == 'POST':
        respuesta_id = request.POST['respuesta']
        examen = get_object_or_404(Exam, pk=examenE_id)
        examen.pregunta_actual += 1
        examen.save()
        cantidad_temas = TemaE.objects.filter(tema_fk=examen).count()
        respuesta = get_object_or_404(Answer, pk=respuesta_id)
        cant_correctas = examen.preguntas_correctas
        if respuesta.es_correcta:
            examen.preguntas_correctas += 1
            temaActual = int(temaActual)
            temaActual += 1
        else:
            randomm = []
            examen.preguntas_incorrectas += 1
        examen.save()
        if temaActual > (cantidad_temas - 1) and cant_correctas < examen.preguntas_correctas:
            temaActual = 0
        return render(request, 'examenes/respuestaE.html',
                      {'respuesta': respuesta, 'examenE': examen, 'temaActual': temaActual})
    examen = get_object_or_404(Exam, pk=examenE_id)
    examen.pregunta_actual += 1
    examen.preguntas_incorrectas += 1
    examen.save()
    return render(request, 'examenes/respuestaE.html', {'examenE': examen, 'temaActual': temaActual})


def examen_view(request):
    """
        Esta funcion muestra las opciones para la configuracion del examen.
        :param request: HttpRequest
        :type: Http
        :return: redirige a un html pasandole dos query
    """
    query = Question.objects.all()
    count = query.count()
    print count
    if count == 0:
        return render(request, 'examenes/preguntasCero.html')
    else:
        return render(request, 'examenes/examen.html',
                      {'list_materias': Materia.objects.values_list('nombre_materia',
                       flat=True).distinct(),
                       'list_temas': Tema.objects.values_list('nombre_tema', flat=True).distinct()})


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
        cantidad_preg_bd += query.count()
    if int(cantidad) > cantidad_preg_bd:
        return render(request, 'examenes/validarCant.html', {'cantidad': cantidad_preg_bd})
    examen = Exam(nombre_materia=materia, cantidad_preg=cantidad, tiempo_preg=tiempo)
    examen.save()
    for i in range(cant_temas):
        nombre_tema = str(tema[i])
        guardar_tema(examen, nombre_tema)
    return render(request, 'examenes/examenencurso.html', {'examen': examen, 'tema_v': tema_vacio, 'temas_v': temas_vacios})


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
        if nota1 == 0:
            examen.porcentaje = 0
            examen.save()
        else:
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
        queryresp = PregResp.objects.filter(examen=examen)
        query = filter_pregunta(result, queryresp)
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
