# -*- coding: utf-8 -*-
from django.shortcuts import render
from lxml import etree
from StringIO import StringIO
from lxml.builder import ElementMaker
from models import Question, Answer
from Levenshtein import *
from django.http import HttpResponse
# Create your views here.

#@login_required
#@permission_required('is_superuser')


def question_view(request):
    """
    Esta clase se utiliza para realizar la creacion de preguntas con sus respectivas respuestas
    parsea un archivo xml, utilizando la libreria LXML. Una vez parseado, se comparan las 
    preguntas existentes utilizando el algoritmo de Levenshtein en la base de datos con las que 
    se quieren crear, si ya existe se da aviso al usuario, si no existen se crean.
    """
    URL_TO_PARSE = '/home/papafrita/Escritorio/XML/preg.xml'
    tree = etree.parse(URL_TO_PARSE)
    root = tree.getroot()
    for pregunta in root:
        materia = pregunta.find('materia').text
        tema = pregunta.find('tema').text
        texto = pregunta.find('texto').text
        if type(texto) == unicode:
            return HttpResponse("La pregunta %s esta mal formada" % texto)
        query = Question.objects.filter(
            nombre_tema=tema).filter(nombre_materia=materia)
        count = query.count()
        #print('el conteo de preguntas con mismo tema y materia: %s' % count)
        if count == 0:
            q = Question(nombre_tema=tema,
                        nombre_materia=materia, text_preg=texto)
            q.save()
            for respuesta in pregunta.iter("respuesta"):
                # print etree.tostring(respuesta)
                text_resp = respuesta.text
                attrib = respuesta.get("estado")
                print attrib
                if attrib is not None:
                    a = Answer(respuesta=q,text_resp=text_resp, es_correcta=True)
                    a.save()
                else:
                    a = Answer(respuesta=q, text_resp=text_resp, es_correcta=False)
                    a.save()
                # print resp_text
                # print attrib
            #print('La pregunta "%s" fue creada' % texto)
        else:
            for i in range(count):
                # print('la i en el bucle es %s' % i)
                repetida = False
                firstObj = query[i]
                #print("Pregunta ya cargada es %s" % firstObj.text_preg)
                #print ("Pregunta que quiero cargar %s" % texto)
                #print(type(firstObj.text_preg))
                #print(type(texto))
                #print('la distancia es %s' %
                #      distance(str(firstObj.text_preg), texto))
                if distance(str(firstObj.text_preg), texto) == 0:
                    repetida = True
                    break
            #print(" La respuesta esta repetida? %r" % repetida)
            if (repetida == False):
                q = Question(nombre_tema=tema,
                            nombre_materia=materia, text_preg=texto)
                q.save()
                #print repetida
                for respuesta in pregunta.iter("respuesta"):
                    resp_text = respuesta.text
                    attrib = respuesta.get("estado")
                    if attrib is not None:
                        a = Answer(respuesta=q, text_resp=resp_text, es_correcta=True)
                        a.save()
                    else:
                        a = Answer(respuesta=q, text_resp=resp_text, es_correcta=False)
                        a.save()
                #print('pregunta "%s" fue creada 2' % texto)
            else:
                print('pregunta "%s" esta repetida' % texto)
    # all_objects = Question.objects.all().delete()
    #print('feo')
    return HttpResponse('se cargo con exito!!')
