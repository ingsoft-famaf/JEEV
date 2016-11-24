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
from django.http import HttpResponse
import json


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


def comparacion_preguntas(string1, string2):
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


def comparacion_distancia(string1, string2):
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


def exist_materia(materia):
    """
    Esta funcion devuelve true o false dependidendo si la materia existe o no.
    :Param materia: String
    :Return: Booleano
    """
    return Materia.objects.filter(nombre_materia=materia).exists()


def exist_tema(tema, materia):
    """
    Esta funcion devuelve true o false dependidendo si el tema existe o no.
    :Param tema: String
    :Param materia: String
    :Return: Booleano
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


def guardarPreg(materia, tema, titulo):
    """
    Esta funcion guarda la pregunta en la base de datos.
    :Param materia: String
    :Param tema: String
    :Param titulo: String
    :Return: el objeto question que fue guardado
    """
    q = Question(nombre_tema=tema, nombre_materia=materia, text_preg=titulo)
    q.save()
    print "la pregunta es: ", q
    return q


def guardar_resp(question, resp):
    """
    Esta funcion guarda la respuesta de una pregunta.
    :Param question: objeto Question
    :Param resp: String
    """
    a = Answer(respuesta=question, text_resp=resp)
    print "se guardo la pregunta: ", a
    a.save()


def agregarPreg(request):
    """
    Esta funcion agrega una nueva pregunta creada por el administrador.
    :Param request: HttpRequest
    :type: Http
    :Return: redirecciona a Http segun corresponda el caso
    """
    if request.method == "POST":
        materia = request.POST['materia']
        tema = request.POST['tema']
        titulo = request.POST['titulo']
        cant_opcion = request.POST['opcion']
        print cant_opcion
        if not exist_materia(materia):
            return render(request, 'questions/MatnoEx.html', {'materia': materia})
        if not exist_tema(tema, materia):
            return render(request, 'questions/TemanoEx.html', {'tema': tema})
        if titulo == "":
            return render(request, 'questions/PregVacio.html')
        if cant_opcion == "":
            return render(request, 'questions/add_sinopc.html')
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
                return render(request, 'questions/repetida.html', {'titulo': titulo})
        opcion = 'opcion'
        opciones = []
        print "aqui mal ", cant_opcion
        for x in xrange(0, int(cant_opcion)):
            try:
                opcion += repr(x)
                opciones.append(request.POST[opcion])
                opcion = 'opcion'
                guardar_resp(q, opciones[x])
                if opciones[x] == "":
                    q.delete()
                    return render(request, 'questions/PregVacio.html')
            except:
                return render(request, 'questions/add_sinopc.html')
        return render(request, 'questions/seguarda.html', {'q': q, 'opciones': opciones, 'parecida': parecida})
    return render(request, 'questions/agregarPreg.html')


def guardarCorrecta(request, question_id):
    """
    Esta funcion guarda la respuesta correcta seleccionada por el administrador,
    de la pregunta nueva que quiere agregar.
    :Param request:HttpRequest
    :Param question_id: Integre
    :Return: redirecciona a Http indicando que se agregó con éxito
    """
    opcion = request.POST['opcion']
    print opcion
    q = get_object_or_404(Question, pk=question_id)
    print "toma  objeto o 404  ", q
    a = Answer.objects.get(respuesta=q, text_resp=opcion)
    print "respuestas ", a
    a.es_correcta = True
    a.save()
    return render(request, 'questions/seagrego.html')


def guardarResp(question, resp, attrib):
    """
    Esta funcion guarda la respuesta
    :Param question: Object
    :Param resp: String
    :Param attrib: String or None
    """
    if attrib is not None:
        a = Answer(respuesta=question, text_resp=resp, es_correcta=True)
        a.save()
    else:
        a = Answer(respuesta=question, text_resp=resp, es_correcta=False)
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
                        tiene_estado += 1
        if tiene_estado < 1 or tiene_estado > 1:
            return False


def validar_yaml(yaml_object):
    """
    Esta funcion devuelve si las respuestas del archivo
    tiene la forma correcta
    :Param string1: objeto yaml
    :Return: Bool
    """
    schema = Schema([{'Materia': str, 'Respuesta': Use(str, int), 'Pregunta': str, 'Tema': str}])
    lista_bloque = []
    index = 0
    try:
        for bloque in yaml.load_all(yaml_object):
            lista_bloque.insert(0, bloque)
            index += 1
    except:
        return False
    else:
        return True


def validar_xml(url):
    """
    Esta funcion devuelve si el archivo
    tiene la forma correcta
    :Param url: string
    :Return: Bool
    """
    XSD_file = 'static/XSD/file.xsd'
    try:
        schema = etree.XMLSchema(file=XSD_file)
        parser = objectify.makeparser(schema=schema)
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
            if tipo == "YAML":
                return upload_question_yaml(request, url)
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
        query = Question.objects.filter(nombre_tema=tema).filter(nombre_materia=materia)
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
                    guardar_resp_dict(resp_dict, q_saved)
            else:
                preguntas_repetidas.insert(index_iguales, pregunta)
                index_iguales += 1
    return render(request, 'questions/secargo_yml.html', {'preguntas': preguntas_repetidas,
                                                          'preguntas_similares': preguntas_parecidas,
                                                          'parecida': parecida, 'repetida': repetida})


def question_view(request, url):
    """
    Esta funcion se utiliza para realizar la creacion de preguntas con sus
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
    index_parecidas = 0
    preguntas_repetidas = []
    preguntas_parecidas = []
    for pregunta in root:
        materia = modificacion_input(pregunta.find('materia').text)
        tema = modificacion_input(pregunta.find('tema').text)
        texto = (pregunta.find('texto').text)
        materia_existe = exist_materia(materia)
        if not materia_existe:
            return render(request, 'questions/noExisteMat.html', {'materia': materia})
        tema_existe = exist_tema(tema, materia)
        if not tema_existe:
            return render(request, 'questions/noExisteTema.html', {'tema': tema})
        if type(texto) == unicode:
            return HttpResponse("La pregunta %s esta mal formada" % texto)
        query = Question.objects.filter(
            nombre_tema=tema).filter(nombre_materia=materia)
        count = query.count()
        parecida = False
        if count == 0:
            qobject = guardarPreg(materia, tema, texto)
            for respuesta in pregunta.iter("respuesta"):
                text_resp = respuesta.text
                attrib = respuesta.get("estado")
                if attrib is not None:
                    guardarResp(qobject, text_resp, attrib)
        else:
            for i in range(count):
                repetida = False
                firstObj = query[i]
                if comparacion_preguntas(str(firstObj.text_preg), texto):
                    repetida = True
                    break
                if es_parecida(str(firstObj.text_preg), texto):
                    parecida = True
            if repetida is False:
                if parecida is True:
                    preguntas_parecidas.insert(index_parecidas, texto)
                    index_parecidas += 1
                qobject = guardarPreg(materia, tema, texto)
                for respuesta in pregunta.iter("respuesta"):
                    resp_text = respuesta.text
                    attrib = respuesta.get("estado")
                    guardarResp(qobject, resp_text, attrib)
            else:
                preguntas_repetidas.insert(index, texto)
                index += 1
    return render(request, 'questions/secargo.html', {'preguntas': preguntas_repetidas,
                                                      'preguntas_similares': preguntas_parecidas,
                                                      'repetida': repetida, 'parecida': parecida})


def buscar_view(request):
    """
    Esta funcion devuelve la lista de todas las preguntas, una vez seleccionada la materia
    se muestran los temas de esa materia.
    :Param request: HttpRequest
    :type: Http
    :Return: redirecciona a Http que corresponda.
    """
    if request.method == "POST":
        materia = str(request.POST['materia'])
        tema = str(request.POST['temas'])
        preguntas = Question.objects.filter(nombre_materia=materia).filter(nombre_tema=tema)
        return render(request, 'questions/listaPreg.html', {'preguntas': preguntas})
    return render(request, 'questions/buscar.html', {'materias': Materia.objects.all()})


def temas(request):
    mat = request.GET['materia']
    materia = get_object_or_404(Materia, nombre_materia=mat)
    temas = Tema.objects.filter(temas=materia)
    temas = [tema.nombre_tema for tema in temas]
    return HttpResponse(json.dumps(temas), content_type="application/json")


def modificar_view(request, question_id):
    """
    Esta funcion da los detalles de una pregunta para modificar.
    :Param request: HttpRequest
    :Param question_id: Integer
    :Return: redirecciona a Http
    """
    pregunta = get_object_or_404(Question, pk=question_id)
    respuestas = Answer.objects.filter(respuesta=pregunta)
    return render(request, 'questions/modificar.html', {'pregunta': pregunta, 'respuestas': respuestas})


def modifiResp(request, question_id, answer_id):
    """
    Esta funcion modifica una respuesta preseleccionada.
    :Param request: HttpRequest
    :Param question_id: Integer
    :Param answer_id: Integer
    :Return: redirecciona a Http
    """
    if request.method == "POST":
        question = get_object_or_404(Question, pk=question_id)
        answer = get_object_or_404(Answer, pk=answer_id)
        resp_nueva = request.POST['nueva_resp']
        answer.text_resp = resp_nueva
        answer.save()
        return render(request, 'questions/modificar.html',
                      {'respuestas': Answer.objects.filter(respuesta=question),
                       'pregunta': question})
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, pk=answer_id)
    return render(request, 'questions/modifiResp.html', {'answer': answer, 'question': question})


def eliminar_resp(request, question_id, answer_id):
    """
    Esta funcion elimina una respuesta preseleccionada.
    :Param request: HttpRequest
    :Param question_id: Integer
    :Param answer_id: Integer
    :Return: redirecciona a Http
    """
    pregunta = get_object_or_404(Question, pk=question_id)
    respuesta = get_object_or_404(Answer, pk=answer_id)
    respuesta.delete()
    return render(request, 'questions/eliminar_resp.html', {'pregunta': pregunta})


def guardar_modif(request, question_id):
    """
    Esta funcion elimina una respuesta preseleccionada.
    :Param request: HttpRequest
    :Param question_id: Integer
    :Return: redirecciona a Http
    """
    q = get_object_or_404(Question, pk=question_id)
    materia = request.POST['materia']
    tema = request.POST['tema']
    titulo = request.POST['textPreg']
    if not exist_materia(materia):
        return render(request, 'questions/mateNE.html', {'materia': materia, 'q': q})
    if not exist_tema(tema, materia):
        return render(request, 'questions/temaNE.html', {'materia': materia, 'tema': tema, 'q': q})
    if titulo == "":
        return render(request, 'questions/textPregVacio.html', {'q': q})
    q.nombre_materia = materia
    q.nombre_tema = tema
    q.text_preg = titulo
    q.save()
    cant_opcion = request.POST['opcion']
    print cant_opcion
    if cant_opcion != "":
        opcion = 'opcion'
        opciones = []
        for x in xrange(int(cant_opcion)):
            opcion += repr(x)
            opciones.append(request.POST[opcion])
            opcion = 'opcion'
            guardar_resp(q, opciones[x])
            if opciones[x] == "":
                q.delete()
                return render(request, 'questions/PregVacio.html')
    respuestas = Answer.objects.filter(respuesta=q)
    return render(request, 'questions/modificado.html', {'pregunta': q, 'respuestas': respuestas})


def reported(request):
    """
    Esta función devuelve una nueva vista con las preguntas que estén reportadas.
    :Param request: HttpRequest
    :type: Http
    :Return: redirecciona a Http
    """
    return render(request, 'questions/reported.html',
                  {'questions': Question.objects.filter(reportada=True)})


def detail_view(request, question_id):
    """
    Esta funcion devuelve una nueva vista con todos los datos de la pregunta.
    :Param request: HttpRequest
    :Param question_id: Integer
    :Return: redirecciona a Http
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'questions/detail.html',
                  {'answers': Answer.objects.filter(respuesta=question),
                   'question': question})


def delete_view(request, question_id):
    """
    Esta funcion se elimina la pregunta preseleccionada.
    correctamenta.
    :Param request: HttpRequest
    :Param question_id: Integer
    :Return: redirecciona a Http
    """
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return render(request, 'questions/delete.html', {})


def update_view(request, question_id, answer_id):
    """
    Esta funcion modifica una respuesta preseleccionada.
    :Param request: HttpRequest
    :Param question_id: Integer
    :Param answer_id: Integer
    :Return: redirecciona a Http
    """
    if request.method == "POST":
        question = get_object_or_404(Question, pk=question_id)
        answer = get_object_or_404(Answer, pk=answer_id)
        resp_nueva = request.POST['new_answer']
        answer.text_resp = resp_nueva
        answer.save()
        return render(request, 'questions/detail.html',
                      {'answers': answer,
                       'question': question})
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, pk=answer_id)
    return render(request, 'questions/update.html',
                  {'answer': answer,
                   'question': question})


def save_view(request, question_id, answer_id):
    """
    Esta funcion guarda la nueva respuesta ingresada, pisando la respuesta anterior preseleccionada.
    :Param request: HttpRequest
    :Param question_id: Integer
    :Param answer_id: Integer
    :Return: redirecciona a Http
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
    Esta funcion saca de la lista de las preguntas reportadas a la pregunta preseleccionada.
    :Param request: HttpRequest
    :Param question_id: Integer
    :Return: redirecciona a Http
    """
    question = get_object_or_404(Question, pk=question_id)
    question.reportada = False
    question.save()
    return render(request, 'questions/reported.html', {'questions': Question.objects.filter(reportada=True)})
