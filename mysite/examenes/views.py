# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from questions.models import Question, Answer
from .models import Exam, PregResp, ExamErrores, PregRespE, TemaE
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

def guardar_Tema(ExamErrores,tema):
    modelTema=TemaE(tema_fk=ExamErrores,nombre_tema=tema)
    modelTema.save()

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

    query = Question.objects.all()
    count = query.count()
    print count
    if count == 0:
        return render(request, 'examenes/preguntasCero.html')
    else:
        query = Materia.objects.values_list(
                                'nombre_materia', flat=True).distinct()
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
    return render(request, 'examenes/selcTemas.html', {'list_temas':list_temas, 'materia':materia})

def examen_encurso(request, materia):
    """
    Algoritmo basado en errores.
    """
 #  pdb.set_trace()
    print ("Print de materia:%s"% materia)
    if request.POST['cantidad'] == "":
        return render(request, 'examenes/datosIncorrectos.html')
    cantidad = request.POST['cantidad']
    print cantidad
    tiempo = request.POST['tiempo']
    examenE = ExamErrores(nombre_materia=materia, 
                cantidad_preg = cantidad, tiempo_preg = tiempo)
    examenE.save()
    tema = request.POST.getlist('tema')
    cant_temas = len(tema)
    print ("print len tema%s" %cant_temas)
    print ("print type tema%s"%type(tema))
    print ("Temas despues de levantarlos %s" % tema)
    print type(tema)
 
    for i in range(cant_temas):
        nombreTema = str(tema[i])
        temas = guardar_Tema(examenE, nombreTema)
    temaActual = 0
    return render(request, 'examenes/encurso.html' ,
                    {'examenE':examenE, 'temaActual':temaActual})


def respPregErrores(request, examenE_id, temaActual):
    """
    Input: HttpRequest y id del examen
    Output: redirige a un html pasándole dos query
    Esta función muestra una pregunta con sus respuestas para que el usuario
    haga la elección de un de ellas.
    """
    print("print de temaActual %s" %temaActual)
    print type(temaActual)
    temaActual = int(temaActual)
    print type(temaActual)
    print("print de temaActual 2 %s" %temaActual)
    examen = get_object_or_404(ExamErrores, pk=examenE_id)
    materia = examen.nombre_materia
    temas = TemaE.objects.filter(tema_fk=examen)
    #nTema = temas[0]
   # print ("print ntema %s" %nTema)
    randomm =[]
    cantidad_temas = temas.count()
    if examen.pregunta_actual == examen.cantidad_preg:
        nota = examen.preguntas_correctas
        nota1 = examen.cantidad_preg
        examen.porcentaje = ((nota * 100) / nota1)
        examen.save()
        return render(request, 'examenes/finalizo.html', {'examen': examen})
    if cantidad_temas == 1:
        nTema = temas[0]
        preguntas = Question.objects.filter(nombre_tema=nTema).filter(nombre_materia=nombreMateria).filter(reportada=False)
    else:
        preguntas= Question.objects.filter(nombre_tema=temas[temaActual]).filter(nombre_materia=materia).filter(reportada=False)
    queryresp = PregRespE.objects.filter(examen=examen)
    query = filter_query(preguntas, queryresp)
    cant_query = query.count()
    print ("query %s" %query)
    if cant_query == 0:
        if temaActual == (cantidad_temas - 1):
            temaActual = 0
            for i in range(cantidad_temas):
                preguntas= Question.objects.filter(nombre_tema=temas[temaActual]).filter(nombre_materia=materia).filter(reportada=False)
                query = filter_query(preguntas, queryresp)
                query_count= query.count()
                if query_count == 0:
                    temaActual +=1 
                else:
                    break
        else:
            temaActual+= 1
        print ("tema actual %s" %temaActual)
        preguntas= Question.objects.filter(nombre_tema=temas[temaActual]).filter(nombre_materia=materia).filter(reportada=False)
        query = filter_query(preguntas, queryresp)
    randomm = random.sample(query, 1)
    pregunta = randomm[0]
    print ("la pregunta es: %s" %pregunta)
    PregRespE.objects.create(examen=examen, question=pregunta)
    return render(request, 'examenes/respPregErrores.html',
                  {'pregunta': pregunta, 'examenE': examen, 'temaActual':temaActual})


def respuestaE(request, examenE_id, temaActual):
    """
    Input: HttpRequest y id del examen
    Output: redirige a un html pasándole una query
    Esta función recoge la respuesta seleccionada y le indica al usuario si
    es correcta o no. Si no responde en el tiempo predeterminado le indica que
    la respuesta es incorrecta.
    """

    print("type temaActual %s" % type(temaActual))
    if request.method == 'POST':
        respuesta_id = request.POST['respuesta']
        examen = get_object_or_404(ExamErrores, pk=examenE_id)
        examen.pregunta_actual +=1
        examen.save()
        cantidad_temas= TemaE.objects.filter(tema_fk=examen).count()
        respuesta = get_object_or_404(Answer, pk=respuesta_id)
        cant_correctas=examen.preguntas_correctas
        if respuesta.es_correcta:
            examen.preguntas_correctas +=1
            temaActual = int(temaActual)
            temaActual +=1
            print("type temaActual  2%s" % type(temaActual))
        else :
            randomm = []
            examen.preguntas_incorrectas +=1
        examen.save()

        print ("examen.preguntas_incorrectas  %s" %examen.preguntas_incorrectas )
        print("temaActual %s" %temaActual)
        print("cantidad_temas - 1 %s" %(cantidad_temas - 1))
        if temaActual > (cantidad_temas - 1) and cant_correctas < examen.preguntas_correctas :
            temaActual = 0

           # if temaActual > cantidad_temas -1:
        return render(request, 'examenes/respuestaE.html',
                      {'respuesta':respuesta, 'examenE':examen, 'temaActual':temaActual})
    examen = get_object_or_404(ExamErrores, pk=examenE_id)
    examen.pregunta_actual +=1
    examen.preguntas_incorrectas +=1
    examen.save()
    print("print de temaActual en respuestaE%s" %temaActual)
    return render(request, 'examenes/respuestaE.html', {'examenE':examen, 'temaActual':temaActual})



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