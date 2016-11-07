# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
#from forms import GetMaterias
from questions.models import Question
from .models import Exam
import questions.models #import Answer
import random
from django.http import HttpResponse


def materia_tema_exist(tema, materia):
#    print(Question.objects.values_list('nombre_materia', flat=True).distinct())
#    print(Question.objects.values_list('nombre_tema', flat=True).distinct())
    return render(request, 'examenes/examen.html',
                  {'list_materias': Question.objects.values_list(
                            'nombre_materia', flat=True).distinct(),
                   'list_temas': Question.objects.values_list(
                            'nombre_tema', flat=True).distinct()})


#   La función examenencurso_view de esta view toman HttpRequest como su primer 
#   parámetro y devuelve una instancia de HttpResponse utilizando el atajo render.
#   Los parámetros de render son request y template_name.

def examenencurso_view(request):
    materia = request.POST['materias']
    tema = request.POST['temas']
    cantidad = request.POST['cantidad']
    tiempo = request.POST['tiempo']
    print 'ifff'
    print materia
    print tema
    print cantidad
    print tiempo
    #preguntas_respondidas = []
    examen = Exam(nombre_materia = materia,nombre_tema = tema,
                    cantidad_preg = cantidad, tiempo_preg = tiempo)
    examen.save()
    print examen.nombre_materia

    """materia = request.POST['materias']
    tema = request.POST['temas']
    cantidad = request.POST['cantidad']
    tiempo = request.POST['tiempo']
    randomint = []
    query = Question.objects.filter(
        nombre_tema=tema).filter(
            nombre_materia=materia).values_list('id', flat=True)
    count = query.count()
    population = query
    cantidadint = int(cantidad)
    """
    return render(request, 'examenes/examenencurso.html' ,
                    {'examen':examen})

def resppreg(request, examen_id):
    examen = get_object_or_404(Exam, pk=examen_id)
    tema = examen.nombre_tema
    materia = examen.nombre_materia
    tiempo = 30
    randomm =[]
    query = Question.objects.filter(
        nombre_tema=tema).filter(
            nombre_materia=materia)
    randomm = random.sample(query, 1)
    #materia = Exam.objects.filter(id=)
    pregunta = randomm[0]
    print pregunta
    return render(request,'examenes/resppreg.html',
                    {'pregunta': pregunta,'timepo':tiempo})

