# -*- coding: utf-8 -*-
import yaml
import xml.etree.ElementTree as ET
from django.shortcuts import render, get_object_or_404
from lxml import etree
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
from schema import Schema, And, Use, Optional
from schema import SchemaError



def es_parecida(string1, string2):
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
    distancia = distance(string1_lower, string2_lower) >= 1 and distance(string1_lower, string2_lower) <= 10
    return distancia

def guardarPreg(materia, tema, titulo):
    """
    Esta funcion guarda en la base de datos la pregunta
    :Param materia: String
    :Param tema: String
    :Param titulo: String
    :Return: Object
    """
    q = Question(nombre_tema=tema, nombre_materia=materia, text_preg=titulo)
    q.save()
    return q

def guardarResp(question, resp, es_correcta, attrib):
    """
    Esta funcion guarda la respuesta
    :Param question: Object
    :Param resp: String
    :Param es_correcta: Bool
    :Param attrib: String or None
    """
    if attrib is not None:
        a = Answer(respuesta=question, text_resp=resp, es_correcta=es_correcta)
        a.save()
    else:
        a = Answer(respuesta=question, text_resp=resp, es_correcta=es_correcta)
        a.save()

def guardar_resp_dict(resp_dict, question):
    """
    Esta funcion guarda la respuesta
    :Param resp_dict: Dict 
    :Param question: Object
    """
    resp = resp_dict.get('correcta')
    if resp is not None:
        a = Answer(respuesta=question, text_resp=resp, es_correcta=True)
        a.save()
    else:
        resp = resp_dict.get('incorrecta')
        a = Answer(respuesta=question, text_resp=resp, es_correcta=False)
        a.save()


def exist_materia(materia):
    """
    Esta funcion comprueba la existencia
    de la materia en la base de datos
    :Param materia: String
    :Return: Bool
    """
    return Materia.objects.filter(nombre_materia=materia).exists()
 

def exist_tema(tema, materia):
    """
    Esta funcion comprueba la existencia
    de la materia en la base de datos
    :Param materia: String
    :Param tema: String
    :Return: Bool
    """
    materias_con_tema = Materia.objects.filter(tema__nombre_tema=tema)
    count_materias = materias_con_tema.count()
    tema_exist = False
    for i in range(count_materias):
        bd_materia = str(materias_con_tema[i])
        if bd_materia == materia:
            tema_exist = True
            break
    return tema_exist

def comparacion_preguntas(string1,string2):
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
    distancia = distance(string1_lower, string2_lower) == 0
    return distancia


def validar_respuestas_yml(objeto):
    """
    Esta funcion devuelve si las respuestas del archivo
    tiene la forma correcta
    :Param string1: objeto yaml
    :Return: Bool
    """
    valido = False
    for bloque in objeto:
        respuestas_lista = bloque.get('Respuesta')
        print respuestas_lista
        count_respuestas = len(respuestas_lista)
        for i in range(count_respuestas):
            resp_dict = respuestas_lista[i]
            resp = resp_dict.get('correcta')
            if resp is not None:
                valido = True
                break
            else:
                valido = False
    return valido
                
def validar_respuestas(root):
    """
    Esta funcion devuelve si las respuestas del archivo
    tiene la forma correcta
    :Param root: String
    :Return: Bool
    """
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

def validar_yaml(yaml_object):
    """
    Esta funcion devuelve si las respuestas del archivo
    tiene la forma correcta
    :Param string1: objeto yaml
    :Return: Bool
    """
    schema = Schema([{'Materia':str,
                  'Respuesta':Use(str,int),
                  'Pregunta':str,
                  'Tema':str}])
    try:
        yml_validacion = yaml.load_all(yaml_object)
        es_valida = True
    except:
        es_valida = False  
    lista_bloque = []
    index = 0
    for bloque in yml_validacion:
        print bloque
        lista_bloque.insert(0,bloque)
        index +=1
        print lista_bloque
    try:
        validated = schema.validate(lista_bloque)
        es_valida = True
    except:
        es_valida = False
    return es_valida

def validar_xml(url):
    """
    Esta funcion devuelve si el archivo
    tiene la forma correcta
    :Param url: string 
    :Return: Bool
    """
    XSD_file = 'static/XSD/file.xsd'
    try:
        schema = etree.XMLSchema(file = XSD_file)
        print schema
        parser = objectify.makeparser(schema = schema)
        boolean = objectify.fromstring(url, parser)
        root = ET.fromstring(url)
        return root
    except XMLSyntaxError:
       return False

def uploadquestion(request):
    """
    Esta funcion crea un string del archivo y lo parsea
    segun el tipo de archivo
    :Param request: request 
    :Return: Bool
    """
    if request.method == 'POST':
        tipo = request.POST['tipo']
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            for chunk in f.chunks():
                url = str() + chunk
                #print url
            print ("El tipo de parseo es %s" % tipo)
            if tipo == "YAML":
                return upload_question_yaml(request,url)  
            else:
                return question_view(request, url)
    else:
        form = UploadFileForm()
    return render(request, 'questions/uploadquestion.html', {'form': form})

def upload_question_yaml(request, url):
    """
    Esta función se utiliza para realizar la creacion de preguntas con sus
    respectivas respuestas parsea un archivo yaml, utilizando la libreria schema.
    Una vez parseado, se comparan las preguntas existentes utilizando el
    algoritmo de Levenshtein en la base de datos con las que se quieren crear,
    si ya existe se da aviso al usuario, si no existen se crean.
    :Param url: String
    :Param request: Request
    :Return: Http
    """
    yml = yaml.load_all(url)
    yml_respuestas = yaml.load_all(url)
    valido = validar_yaml(url)
    if valido is False:
        return render(request, 'questions/invalido_YAML.html')
    respuestas_validas = validar_respuestas_yml(yml_respuestas)
    if respuestas_validas is False:
        return render(request, 'questions/resp_invalida.html')
    index_iguales = 0
    index_parecidas = 0
    preguntas_repetidas = []
    preguntas_parecidas = []
    for block in yml:
        materia = modificacion_input(block.get('Materia'))
        tema = modificacion_input(block.get('Tema'))
        pregunta = block.get('Pregunta')
        respuestas_lista = block.get('Respuesta')
        materia_existe = exist_materia(materia)
        if not materia_existe:
            return render(request, 'questions/noExisteMat.html', {'materia': materia})
        tema_existe = exist_tema(tema, materia)
        if not tema_existe:
            return render(request, 'questions/noExisteTema.html', {'tema': tema})
        query = Question.objects.filter(
            nombre_tema=tema).filter(nombre_materia=materia)
        count = query.count()
        count_respuestas = len(respuestas_lista)
        parecida = False
        if count == 0:
            qobject = guardarPreg(materia, tema, pregunta)
            for i in range(count_respuestas):
                resp_dict = respuestas_lista[i]
                guardar_resp_dict(resp_dict, qobject)
        else:
            for i in range(count):
                repetida = False
                firstObj = query[i]
                if comparacion_preguntas(str(firstObj.text_preg), pregunta):
                    repetida = True
                    break
                if es_parecida(str(firstObj.text_preg), pregunta):
                    parecida = True
            if repetida is False:
                if parecida is True:
                    preguntas_parecidas.insert(index_parecidas, pregunta)
                    index_parecidas += 1
                q_saved = guardarPreg(materia, tema, pregunta)
                for i in range(count_respuestas):
                    resp_dict = respuestas_lista[i]
                    guardar_resp_dict(resp_dict,q_saved)
            else:
                preguntas_repetidas.insert(index_iguales, pregunta)
                index_iguales +=  1
    return render(request, 'questions/secargo_yml.html', {'preguntas': preguntas_repetidas, 'preguntas_similares': preguntas_parecidas})

def question_view(request, url):
    """
    Esta función se utiliza para realizar la creacion de preguntas con sus
    respectivas respuestas parsea un archivo xml, utilizando la libreria LXML.
    Una vez parseado, se comparan las preguntas existentes utilizando el
    algoritmo de Levenshtein en la base de datos con las que se quieren crear,
    si ya existe se da aviso al usuario, si no existen se crean.
    :Param url: String
    :Param request: Request
    :Return: Http
    """
    root = validar_xml(url)
    if root is False:
        return render(request, 'questions/invalido_XML.html')
    respuestas_validas = validar_respuestas(root)
    if respuestas_validas is False:
        return render(request, 'questions/resp_invalida.html')
    index = 0
    preguntas_repetidas = []
    for pregunta in root:
        materia =modificacion_input(pregunta.find('materia').text)
        tema = modificacion_input(pregunta.find('tema').text)
        texto = (pregunta.find('texto').text)
        materia_exists = Materia.objects.filter(
            nombre_materia=materia).exists()
        if not materia_exists:
            return render(request, 'questions/noExisteMat.html', {'materia': materia})
        materias_con_tema = Materia.objects.filter(tema__nombre_tema=tema)
        count_materias = materias_con_tema.count()
        tema_exist = False
        for i in range(count_materias):
            bd_materia = str(materias_con_tema[i])
            if bd_materia == materia:
                tema_exist = True
                break
        if not tema_exist:
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
                if comparacion_preguntas(str(firstObj.text_preg), texto):
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
                preguntas_repetidas.insert(index, texto)
                index += 1
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
