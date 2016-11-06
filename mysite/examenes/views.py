from django.shortcuts import render, get_object_or_404
#from forms import GetMaterias
from questions.models import Question, Answer
from .models import Exam
import questions.models #import Answer
import random
from django.http import HttpResponse

def examen_view(request):
#    print(Question.objects.values_list('nombre_materia', flat=True).distinct())
#    print(Question.objects.values_list('nombre_tema', flat=True).distinct())

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
#    print 'ifff'
#    print materia
#    print tema
#    print cantidad
    print tiempo
    #preguntas_respondidas = []
    examen = Exam(nombre_materia = materia,nombre_tema = tema,
                    cantidad_preg = cantidad, tiempo_preg = tiempo)
    examen.save()
#    print examen.nombre_materia

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
        return render(request, 'examenes/finalizo.html')
    return render(request,'examenes/resppreg.html',
                  {'pregunta': pregunta,'examen':examen})

def respuesta(request, examen_id):

    if request.method == 'POST':
        respuesta_id = request.POST['respuesta']
        examen = get_object_or_404(Exam, pk=examen_id)
        examen.pregunta_actual +=1
        examen.save()
        respuesta = get_object_or_404(Answer, pk=respuesta_id)
        return render(request, 'examenes/respuesta.html',
                      {'respuesta':respuesta, 'examen':examen})
    examen = get_object_or_404(Exam, pk=examen_id)
    return render(request, 'examenes/respuesta.html', {'examen':examen})

def reportar(request, examen_id, pregunta_id):
    examen = get_object_or_404(Exam, pk=examen_id)
    pregunta = get_object_or_404(Question, pk=pregunta_id)
    pregunta.reportada = True
    pregunta.save()
    return render(request, 'examenes/respuesta.html',
                  {'pregunta': pregunta, 'examen': examen})
