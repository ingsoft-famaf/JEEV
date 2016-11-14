# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from questions.models import Question, Answer
from .models import Exam
import questions.models
import random
from django.http import HttpResponse

def examen_view(request):
    """
    Esta función muestra las opciones para la configuración del examen.
    :param request: HttpRequest
    :type: Http
    :return: redirige a un html pasándole dos query
    """
    return render(request, 'examenes/examen.html',
                  {'list_materias': Question.objects.values_list(
                            'nombre_materia', flat=True).distinct(),
                   'list_temas': Question.objects.values_list(
                            'nombre_tema', flat=True).distinct()})

def examenencurso_view(request):
    """
    Esta función recoge la configuración del usuario y le indica al usuario
    que la configuración se realizó correctamente.
    :param request: HttpRequest
    :return: redirige a un html pasándole una query
    """
    materia = request.POST['materias']
    tema = request.POST['temas']
    cantidad = request.POST['cantidad']
    tiempo = request.POST['tiempo']
    examen = Exam(nombre_materia = materia,nombre_tema = tema,
                    cantidad_preg = cantidad, tiempo_preg = tiempo)
    examen.save()

    return render(request, 'examenes/examenencurso.html' ,
                    {'examen':examen})

def resppreg(request, examen_id):
    """
    Esta función muestra una pregunta con sus respuestas para que el usuario
    haga la elección de un de ellas.
    :Param  request: HttpRequest 
    :Param examen_id: id del examen
    :return: redirige a un html pasándole dos query
    """
    examen = get_object_or_404(Exam, pk=examen_id)
    tema = examen.nombre_tema
    materia = examen.nombre_materia
    cantidad = examen.cantidad_preg
    cantidad = int(cantidad)
    randomm =[]
    query1 = Question.objects.filter(nombre_tema=tema)
    query2 = query1.filter(nombre_materia=materia)
    query3 = query2.filter(reportada=False)
    randomm = random.sample(query3, 1)
    #materia = Exam.objects.filter(id=)
    pregunta = randomm[0]
#    print examen.pregunta_actual
#    print examen.cantidad_preg
    if examen.pregunta_actual == examen.cantidad_preg:
        return render(request, 'examenes/finalizo.html',
                      {'examen': examen})
    return render(request,'examenes/resppreg.html',
                  {'pregunta': pregunta,'examen':examen})

def respuesta(request, examen_id):
    """
    Esta función recoge la respuesta seleccionada y le indica al usuario si 
    es correcta o no. Si no responde en el tiempo predeterminado le indica que
    la respuesta es incorrecta.
    :Param request: HttpRequest 
    :Param examen_id: id del examen
    :return: redirige a un html pasándole una query
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
    Esta función le indica al usuario que la pregunta fue reportada.
    :Param request: HttpRequest
    :Param examen_id: id del examen 
    :Param pregunta_id: id de la pregunta
    :retun: redirige a un html pasándole dos query
    """
    examen = get_object_or_404(Exam, pk=examen_id)
    pregunta = get_object_or_404(Question, pk=pregunta_id)
    pregunta.reportada = True
    pregunta.save()
    return render(request, 'examenes/respuesta.html',
                  {'pregunta': pregunta, 'examen': examen})
