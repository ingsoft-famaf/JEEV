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
from materias.models import Materia, Tema
from lxml import etree, objectify
from lxml.etree import XMLSyntaxError
from materias.views import modificacion_input


def comparacion_preguntas(string1,string2):
    """
    Esta funcion devuelve la distancia de Levenshtein entre
    dos strings sin espacios y en minuscula
    :Param string1: String
    :Param string2: String
    :Return: String
    """
    #print string1
    #print string2
    string2_joined = "".join(string2.split())
    string1_joined = "".join(string1.split())
    #print string1_joined
    #print string2_joined 
    string1_lower = string1_joined.lower()
    string2_lower = string2_joined.lower()
    #print ("String1_lower es %s" % string1_lower)
    #print ("String2_lower es %s" % string2_lower)
    distancia = distance(string1_lower, string2_lower) == 0
    #print distancia
    return distancia

def comparacion_distancia(string1,string2):
    """
    Esta funcion devuelve la distancia de Levenshtein entre
    dos strings sin espacios y en minuscula
    :Param string1: String
    :Param string2: String
    :Return: String
    """
    string2_joined = "".join(string2.split())
    string1_joined = "".join(string1.split())
    string1_lower = string1_joined.lower()
    string2_lower = string2_joined.lower()
    distancia = distance(string1_lower, string2_lower) >=1 and distance(string1_lower, string2_lower) <=10
    #print distancia
    return distancia


def exist_materia(materia):
    return Materia.objects.filter(nombre_materia=materia).exists()

def exist_tema(tema, materia):
    materias_con_tema = Materia.objects.filter(tema__nombre_tema=tema)
    count_materias = materias_con_tema.count()
    tema_exist = False
    for i in range(count_materias):
        bd_materia = str(materias_con_tema[i])
        if bd_materia == materia:
            tema_exist = True
            break
    return tema_exist


def guardarPreg(materia, tema, titulo):
    q = Question(nombre_tema=tema, nombre_materia=materia, text_preg=titulo)
    q.save()
    return q

def guardarResp(question, resp):
    a = Answer(respuesta=question, text_resp=resp)
    a.save()


def agregarPreg(request):
    if request.method == "POST":
        materia = request.POST['materia']
        tema = request.POST['tema']
        titulo = request.POST['titulo']
        cant_opcion = request.POST['opcion']
        if not exist_materia(materia):
            return render(request, 'questions/MatnoEx.html', {'materia': materia})
        if not exist_tema(tema, materia):
            return render(request, 'questions/TemanoEx.html', {'tema': tema})
        parecida = False
        query = Question.objects.filter(nombre_tema=tema).filter(nombre_materia=materia)
        count = query.count()
        if count == 0:
            q = guardarPreg(materia, tema, titulo)
        else:
            for i in range(count):
                repetida = False
                firstObj = query[i]
                if comparacion_preguntas(str(firstObj.text_preg), str(titulo)):
                    repetida = True
                    break
                if comparacion_distancia(str(firstObj.text_preg), str(titulo)):
                    parecida = True
            if repetida is False:
                q = guardarPreg(materia, tema, titulo)
            else:
                return render(request, 'questions/repetida.html', {'titulo':titulo})
        opcion = 'opcion'
        opciones = []
        for x in xrange(0,int(cant_opcion)):
            opcion += `x`
            opciones.append(request.POST[opcion])
            opcion = 'opcion'
            guardarResp(q, opciones[x])
        return render(request, 'questions/seguarda.html', {'q':q, 'opciones': opciones, 'parecida': parecida})
    return render(request, 'questions/agregarPreg.html')

def guardarCorrecta(request, question_id):
    opcion = request.POST['opcion']
    q = get_object_or_404(Question, pk=question_id)
    a = Answer.objects.get(respuesta=q, text_resp=opcion)
    a.es_correcta = True
    a.save()
    return render(request, 'questions/seagrego.html')


def validar_respuestas(root):
    for pregunta in root:
        tiene_estado = 0
        for respuesta in pregunta.iter("respuesta"):
                    resp_text = respuesta.text
                    attrib = respuesta.get("estado")
                    if attrib is not None:
                        print ("la respuestas %s tiene estado" % respuesta.text)
                        tiene_estado += 1
        print ("tiene_estado es %s" % tiene_estado)
        if tiene_estado <1 or tiene_estado >1:
            return False


def validar(url):
    XSD_file = 'static/XSD/file.xsd'
    #with open('static/XSD/file.xsd', 'r') as f:
    #    schema_root = etree.parse(f)
    #import pdb
    #pdb.set_trace()
    try:
        schema = etree.XMLSchema(file = XSD_file)
        print schema
        parser = objectify.makeparser(schema = schema)
        boolean = objectify.fromstring(url, parser)
        root = ET.fromstring(url)
        return root
    except XMLSyntaxError:
       return False
#    parser = etree.XMLParser(schema = schema)
    #return schema.validate(url)
    #    try:
#        etree.fromstring(url, parser)
#        return root
#    except etree.XMLSchemaError:
#        return HttpResponse('El formato del xml no es el correcto')
#    except XMLSyntaxError:
#        return HttpResponse('mal formato')

def uploadquestion(request):
    """

    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            for chunk in f.chunks():
                url = str() + chunk
            # print url
            return question_view(request, url)
    else:
        form = UploadFileForm()
    return render(request, 'questions/uploadquestion.html', {'form': form})


def question_view(request, url):
    """
    Esta función se utiliza para realizar la creacion de preguntas con sus
    respectivas respuestas parsea un archivo xml, utilizando la libreria LXML.
    Una vez parseado, se comparan las preguntas existentes utilizando el
    algoritmo de Levenshtein en la base de datos con las que se quieren crear,
    si ya existe se da aviso al usuario, si no existen se crean.
    """
    root = validar(url)
    if root is False:
        return render(request, 'questions/invalido.html')
    respuestas_validas = validar_respuestas(root)
    if respuestas_validas is False:
        return render(request, 'questions/resp_invalida.html')
    index = 0
    preguntas_repetidas = []
    for pregunta in root:
        materia = pregunta.find('materia').text
        tema = pregunta.find('tema').text
        texto = pregunta.find('texto').text
        if not exist_materia(materia):
            return render(request, 'questions/noExisteMat.html', {'materia': materia})
        if not exist_tema(tema):
            return render(request, 'questions/noExisteTema.html', {'tema': tema})
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
                if distance(str(firstObj.text_preg), texto) <= 0:
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
                preguntas_repetidas.insert(index,texto)
                index +=  1
    return render(request, 'questions/secargo.html', {'preguntas':preguntas_repetidas})


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
