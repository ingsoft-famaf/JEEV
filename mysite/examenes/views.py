from django.shortcuts import render
#from forms import GetMaterias
from questions.models import Question
import questions.models #import Answer
import random
from django.http import HttpResponse

def examen_view(request):
    print(Question.objects.values_list('nombre_materia', flat=True).distinct())
    print(Question.objects.values_list('nombre_tema', flat=True).distinct())
    return render(request, 'examenes/examen.html',
                  {'list_materias': Question.objects.values_list(
                            'nombre_materia', flat=True).distinct(),
                   'list_temas': Question.objects.values_list(
                            'nombre_tema', flat=True).distinct()})

def examenencurso_view(request):
    materia = request.POST['materias']
    tema = request.POST['temas']
    cantidad = request.POST['cantidad']
    tiempo = request.POST['tiempo']
    randomint = []
    query = Question.objects.filter(
        nombre_tema=tema).filter(
            nombre_materia=materia).values_list('id', flat=True)
    count = query.count()
    population = query
    #print query
    if cantidad <= count:
        randomint = random.sample(population, int(cantidad))
        print randomint
        preguntas = Question.objects.filter(
            nombre_tema=tema).filter(nombre_materia=materia).filter(
            pk__in=randomint)
        return render(request,'examenes/examenencurso.html',
                        {'preguntas': preguntas}, {'tiempo': tiempo})
    else:
        preguntas = Question.objects.filter(
            nombre_tema=tema).filter(
                nombre_materia=materia).all()
        return render(request, 'examenes/examenencurso.html' ,
                        {'preguntas': preguntas, 'tiempo': tiempo})
