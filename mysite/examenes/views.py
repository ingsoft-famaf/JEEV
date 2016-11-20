# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from questions.models import Question, Answer
from .models import Exam, PregResp, ExamErrores
import questions.models #import Answer
import random
from materias.models import Materia, Tema
from django.http import HttpResponse
import pdb

"""aux functions"""
#def question_random
def filter_query (realquery, querytofilt):
    for q in querytofilt:
        for q2 in realquery:
            if q.question.id == q2.id :
                realquery = realquery.exclude(id = q2.id)
    return realquery
"""End aux functions"""

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
    query = Materia.objects.values_list(
                            'nombre_materia', flat=True).distinct()
    print query
    return render(request, 'examenes/selcMateria.html',
                  {'list_materias': Materia.objects.values_list(
                            'nombre_materia', flat=True).distinct()})

def selcTemas(request):
    """
    Input: HttpRequest
    Output: redirige a un html pasándole dos query
    Esta función muestra las opciones de temas para la configuración del examen
    para el algoritmo basado en errores.
    """
    materia = request.POST['materias']
    list_temas= Tema.objects.values_list(
                            'nombre_tema',flat=True).filter(temas__nombre_materia=materia)
    return render(request, 'examenes/selcTemas.html', {'list_temas':list_temas})

def examen_encurso(request):
    """
    Algoritmo basado en errores.
    """
    if request.POST['cantidad'] == "":
        return render(request, 'examenes/datosIncorrectos.html')
   # tema = []
    tema = request.POST.getlist('tema.id')
    print "ESTOY ACA"
    print tema
    cantidad = request.POST['cantidad']
    print cantidad
    tiempo = request.POST['tiempo']
    examen = ExamErrores(nombre_tema = tema,cantidad_preg = cantidad, tiempo_preg = tiempo)
    examen.save()
    return render(request, 'examenes/encurso.html' ,
                    {'examen':examen})


""" Algoritmo aleatorio"""
def examen_view(request):
    """
    Input: HttpRequest
    Output: redirige a un html pasándole dos query
    Esta función muestra las opciones para la configuración del examen.
    """
    query = Question.objects.all()
    count = query.count()
    print count
    if count == 0:
        return render(request, 'examenes/preguntasCero.html')
    else:
        return render(request, 'examenes/examen.html',
                  {'list_materias': Materia.objects.values_list(
                            'nombre_materia', flat=True).distinct(),
                   'list_temas': Tema.objects.values_list(
                            'nombre_tema', flat=True).distinct()})


def examenencurso_view(request):
    """
    Input: HttpRequest
    Output: redirige a un html pasándole una query
    Esta función recoge la configuración del usuario y le indica al usuario
    que la configuración se realizó correctamente.
    """
    if request.POST['cantidad'] == "":
        return render(request, 'examenes/datosIncorrectos.html')
    materia = request.POST['materias']
    tema = request.POST['temas']
    query = Question.objects.filter(nombre_tema=tema)
    count = query.count()
    print "count de cantidad de temas"
    print count
    if count == 0:
        return render(request, 'examenes/TemaSinPreguntas.html')
    else: 
        cantidad = request.POST['cantidad']
        tiempo = request.POST['tiempo']
        examen = Exam(nombre_materia = materia,nombre_tema = tema,
                        cantidad_preg = cantidad, tiempo_preg = tiempo)
        examen.save()
        return render(request, 'examenes/examenencurso.html' ,
                        {'examen':examen})

def resppreg(request, examen_id):
    """
    Input: HttpRequest y id del examen
    Output: redirige a un html pasándole dos query
    Esta función muestra una pregunta con sus respuestas para que el usuario
    haga la elección de un de ellas.
    """
    examen = get_object_or_404(Exam, pk=examen_id)
    tema = examen.nombre_tema
    materia = examen.nombre_materia
    randomm =[]
    query1 = Question.objects.filter(nombre_tema=tema)
    query2 = query1.filter(nombre_materia=materia)
    query3 = query2.filter(reportada=False)
    #si pide mas preguntas de las que tenemos disminuimos la cantidad
    #para no generar conflictos de bordes
    if examen.cantidad_preg > query3.count():
        examen.cantidad_preg = query3.count()

    print examen.cantidad_preg
    if examen.pregunta_actual == examen.cantidad_preg:
        return render(request, 'examenes/finalizo.html',
                      {'examen': examen})
    print examen.cantidad_preg
    #query con las respuestas ya respondidas
    queryresp = PregResp.objects.filter(examen = examen)
    #se filtran las ya respondidas
    query3 = filter_query(query3,queryresp)
    randomm = random.sample(query3, 1)
    pregunta = randomm[0]
    PregResp.objects.create(examen = examen, question = pregunta)

    return render(request,'examenes/resppreg.html',
                  {'pregunta': pregunta,'examen':examen})

def respuesta(request, examen_id):
    """
    Input: HttpRequest y id del examen
    Output: redirige a un html pasándole una query
    Esta función recoge la respuesta seleccionada y le indica al usuario si
    es correcta o no. Si no responde en el tiempo predeterminado le indica que
    la respuesta es incorrecta.
    """
    if request.method == 'POST':
        respuesta_id = request.POST['respuesta']
        examen = get_object_or_404(Exam, pk=examen_id)
        examen.pregunta_actual +=1
        examen.save()
        respuesta = get_object_or_404(Answer, pk=respuesta_id)
        if respuesta.es_correcta:
            examen.preguntas_correctas +=1
        else :
            examen.preguntas_incorrectas +=1
        examen.save()
        return render(request, 'examenes/respuesta.html',
                      {'respuesta':respuesta, 'examen':examen})
    examen = get_object_or_404(Exam, pk=examen_id)
    examen.pregunta_actual +=1
    examen.preguntas_incorrectas +=1
    examen.save()
    return render(request, 'examenes/respuesta.html', {'examen':examen})

def reportar(request, examen_id, pregunta_id):
    """
    Input: HttpRequest, id del examen y id de la pregunta
    Output: redirige a un html pasándole dos query
    Esta función le indica al usuario que la pregunta fue reportada.
    """
    examen = get_object_or_404(Exam, pk=examen_id)
    pregunta = get_object_or_404(Question, pk=pregunta_id)
    pregunta.reportada = True
    pregunta.save()
    return render(request, 'examenes/respuesta.html',
                  {'pregunta': pregunta, 'examen': examen})
