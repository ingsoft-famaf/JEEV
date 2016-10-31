from django.shortcuts import render
#from forms import GetMaterias
from questions.models import Question
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
    randomint = []
    query = Question.objects.filter(
        nombre_tema=tema).filter(
            nombre_materia=materia).values_list('id', flat=True)
    count = query.count()
    population = query
    print query
    if cantidad <= count:
        randomint = random.sample(population, int(cantidad))
        print randomint
        preguntas = Question.objects.filter(
            nombre_tema=tema).filter(nombre_materia=materia).filter(
            pk__in=randomint).values_list('text_preg', flat=True)
        print preguntas
        return render(request,'examenes/examenencurso.html',
                        {'preguntas': preguntas})
    else:
        preguntas = Question.objects.filter(
            nombre_tema=tema).filter(
                nombre_materia=materia).all().values_list('text_preg', flat=True)
        print preguntas
        return render(request, 'examenes/examenencurso.html' ,
                        {'preguntas': preguntas})

def responder_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'examenes/responder.html',
                  {'answers': Answer.objects.filter(respuesta=question),
                   'question': question})
