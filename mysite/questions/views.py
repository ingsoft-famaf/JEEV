# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from lxml import etree
import xml.etree.ElementTree as ET
from StringIO import StringIO
from lxml.builder import ElementMaker
from models import Question, Answer
from Levenshtein import *
from django.http import HttpResponse
from .forms import UploadFileForm


def uploadquestion(request):
    """
    
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            for chunk in f.chunks():
                url = str() + chunk
            print url
            return question_view(url)
    else:
        form = UploadFileForm()
    return render(request, 'questions/uploadquestion.html', {'form': form})


def question_view(url):
    """
    Esta función se utiliza para realizar la creacion de preguntas con sus
    respectivas respuestas parsea un archivo xml, utilizando la libreria LXML.
    Una vez parseado, se comparan las preguntas existentes utilizando el
    algoritmo de Levenshtein en la base de datos con las que se quieren crear,
    si ya existe se da aviso al usuario, si no existen se crean.
    """
    root = ET.fromstring(url)
    for pregunta in root:
        materia = pregunta.find('materia').text
        tema = pregunta.find('tema').text
        texto = pregunta.find('texto').text
        if type(texto) == unicode:
            return HttpResponse("La pregunta %s esta mal formada" % texto)
        query = Question.objects.filter(
            nombre_tema=tema).filter(nombre_materia=materia)
        count = query.count()
        if count == 0:
            q = Question(nombre_tema=tema,
                         nombre_materia=materia, text_preg=texto,
                         reportada=False)
            q.save()
            for respuesta in pregunta.iter("respuesta"):
                text_resp = respuesta.text
                attrib = respuesta.get("estado")
                print attrib
                if attrib is not None:
                    a = Answer(respuesta=q, text_resp=text_resp,
                               es_correcta=True)
                    a.save()
                else:
                    a = Answer(respuesta=q, text_resp=text_resp,
                               es_correcta=False)
                    a.save()
        else:
            for i in range(count):
                repetida = False
                firstObj = query[i]
                if distance(str(firstObj.text_preg), texto) == 0:
                    repetida = True
                    break
            if repetida is False:
                q = Question(nombre_tema=tema,
                             nombre_materia=materia, text_preg=texto,
                             reportada=False)
                q.save()
                for respuesta in pregunta.iter("respuesta"):
                    resp_text = respuesta.text
                    attrib = respuesta.get("estado")
                    if attrib is not None:
                        a = Answer(respuesta=q, text_resp=resp_text,
                                   es_correcta=True)
                        a.save()
                    else:
                        a = Answer(respuesta=q, text_resp=resp_text,
                                   es_correcta=False)
                        a.save()
            else:
                print('pregunta "%s" esta repetida' % texto)
    return HttpResponse('Las preguntas se cargaron con exito!!')


def reported(request):
    """
    Esta función redirecciona la vista a un html pasandole sólo las preguntas
    que estén reportadas, el html motrará una lista de esas preguntas.
    """
    return render(request, 'questions/reported.html',
                  {'questions': Question.objects.filter(reportada=True)})


def detail_view(request, question_id):
    """
    Esta función toma el id de la pregunta y la busca en la base de datos,
    sino se encuentra devuelve un error 404. Redirecciona la vista a un html
    con todos respuestas de la pregunta seleccionada cada una con un botón
    para modificarla y un botón general para eliminar la pregunta con sus
    respectivas respuestas completa.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'questions/detail.html',
                  {'answers': Answer.objects.filter(respuesta=question),
                   'question': question})


def delete_view(request, question_id):
    """
    Esta función toma el id de la pregunta y la busca en la base de datos,
    sino se encuentra devuelve un error 404, elimana esa pregunta y
    redirecciona la vista a un html que le informa al usuario que se eliminó
    correctamenta.
    """
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return render(request, 'questions/delete.html', {})


def update_view(request, question_id, answer_id):
    """
    Esta función toma el id de la pregunta y el id de una respuesta y las busca
    en la base de datos, sino se encuentran devuelve un error 404. Redirecciona
    la vista a un html en donde este muestra la respuesta que se seleccionó
    para modificar y le inidca al usuario que ingrese la nueva respuesta.
    """
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, pk=answer_id)
    return render(request, 'questions/update.html',
                  {'answer': answer,
                   'question': question})


def save_view(request, question_id, answer_id):
    """
    Esta función toma el id de la pregunta y el id de una respuesta y las busca
    en la base de datos, sino se encuentran devuelve un error 404. Toma la
    nueva respuesta que ingresó el usuario, la coloca en el campo text_resp de
    la respuesta y lo guarda. Redirecciona la vista al html en donde esta la
    pregunta con sus respectivas respuestas pero esta vez con la respuesta que
    se modificó actualizada.
    """
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, pk=answer_id)
    resp_nueva = request.POST['new_answer']
    answer.text_resp = resp_nueva
    answer.save()
    return render(request, 'questions/detail.html',
                  {'answers': Answer.objects.filter(respuesta=question),
                   'question': question})


def sacardereported(request, question_id):
    """
    Esta función toma el id de la pregunta y la busca en la base de datos,
    sino se encuentra devuelve un error 404. CAmbia el estado de reportada
    a falso, sacándola así de la lista de las preguntas reportadas.
    Redirecciona la vista a la lista de las preguntas reportadas.
    """
    question = get_object_or_404(Question, pk=question_id)
    question.reportada = False
    question.save()
    return render(request, 'questions/reported.html',
                  {'questions': Question.objects.filter(reportada=True)})

