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
        bla = str(tema[i])
        temas = TemaE(tema_fk=examenE, nombre_tema=bla)
        temas.save()
        print ("print type i%s" %type(i))
        print ("print i %s" %i)
    
    print ("print temas de examen %s "% TemaE.objects.filter(tema_fk=examenE))
    print type(TemaE.nombre_tema)
    return render(request, 'examenes/encurso.html' ,
                    {'examenE':examenE})


def respPregErrores(request, examenE_id):
    """
    Input: HttpRequest y id del examen
    Output: redirige a un html pasándole dos query
    Esta función muestra una pregunta con sus respuestas para que el usuario
    haga la elección de un de ellas.
    """
    examen = get_object_or_404(ExamErrores, pk=examenE_id)
    
    query = examen.nombre_materia
    print ("respPregErrores primera query: %s" % query)
    tema1 = examen.nombre_tema
    test = []
    test = [x.encode('UTF8') for x in tema1]
    print "prueba test"
    print type(test)
    print test
    query_list = []
    nueva_lista = []
    
    print ("tema1 en el examen: %s"% tema1)
 #   count_temas = 0
    randomm =[]
    count_temas = len(tema1)
  #  count_temas = 2
    list_preguntas_count=[]
    print ("count_temas es %s" % count_temas)

    for i in range(count_temas):
        queryQ = Question.objects.filter(nombre_tema=str(tema1[i])).filter(nombre_materia=query)
        query_list.insert(i,queryQ)
        print ("print queryQ: %s"% queryQ)
    print ("print query_list[0]: %s"% query_list[0])

    largo2 = 0
    for k in range(count_temas):   
        largo1= query_list[k].count()
        print largo1
        largo2 += largo1
    print ("el largo2 es %s" % largo2)
    #si pide mas preguntas de las que tenemos disminuimos la cantidad
    #para no generar conflictos de bordes
    print ("print examen.cantidad_preg: %s"% examen.cantidad_preg)
    if examen.cantidad_preg > largo2:
        examen.cantidad_preg = largo2

    print examen.cantidad_preg
    print ("la pregunta_actual es %s" % examen.pregunta_actual) 
    if examen.pregunta_actual == examen.cantidad_preg:
        return render(request, 'examenes/finalizo.html',
                      {'examenE': examen})
    print examen.cantidad_preg
    #query con las respuestas ya respondidas
    queryresp = PregRespE.objects.filter(examen = examen)
    print ("queryresp %s" % queryresp)
    #se filtran las ya respondidas
    querys = filter_query(largo2,queryresp)
    randomm = random.sample(querys, 1)
    pregunta = randomm[0]
    PregRespE.objects.create(examenE = examen, question = pregunta)

    return render(request,'examenes/respPregErrores.html',
                  {'pregunta': pregunta,'examenE':examen})


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