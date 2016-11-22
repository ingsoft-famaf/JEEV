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
    return q


def guardar_resp(question, resp):
    """
    Esta funcion guarda la respuesta de una pregunta.
    :Param question: objeto Question
    :Param resp: String
    """
    a = Answer(respuesta=question, text_resp=resp)
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
        if not exist_materia(materia):
            return render(request, 'questions/MatnoEx.html', {'materia': materia})
        if not exist_tema(tema, materia):
            return render(request, 'questions/TemanoEx.html', {'tema': tema})
        if titulo == "":
            return render(request, 'questions/PregVacio.html')
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
        for x in xrange(0, int(cant_opcion)):
            opcion += repr(x)
            opciones.append(request.POST[opcion])
            opcion = 'opcion'
            guardar_resp(q, opciones[x])
            if opciones[x] == "":
                q.delete()
                return render(request, 'questions/PregVacio.html')
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
                        tiene_estado += 1
        if tiene_estado < 1 or tiene_estado > 1:
            return False


def validar(url):
    XSD_file = 'static/XSD/file.xsd'
    try:
        schema = etree.XMLSchema(file=XSD_file)
        print schema
        parser = objectify.makeparser(schema=schema)
        boolean = objectify.fromstring(url, parser)
        root = ET.fromstring(url)
        return root
    except XMLSyntaxError:
        return False


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
                preguntas_repetidas.insert(index, texto)
                index += 1
    return render(request, 'questions/secargo.html', {'preguntas': preguntas_repetidas})


def buscar_view(request):
    """
    Esta funcion devuelve la lista de todas las preguntas, una vez seleccionada la materia
    se muestran los temas de esa materia.
    :Param request: HttpRequest
    :type: Http
    :Return: redirecciona a Http que corresponda.
    """
    if request.method == "POST":
        mat = request.POST['materia']
        materia = get_object_or_404(Materia, pk=mat)
        temas = Tema.objects.filter(temas=materia)
        return render(request, 'questions/buscarT.html', {'materia': materia, 'temas': temas})
    return render(request, 'questions/buscar.html', {'materias': Materia.objects.all()})


def temas(request):
    mat = request.POST['materia']
    materia = get_object_or_404(Materia, nombre_materia=mat)
    temas = Tema.objects.filter(temas=materia)
    print temas
    return render(request, {'temas': temas})


def lista_view(request, materia_id):
    """
    Esta funcion da la lista de los temas sólos los de la materia preseleccionada.
    :Param request: HttpRequest
    :type: Http
    :Return: redirecciona a Http 
    """
    if request.method == "POST":
        materia = get_object_or_404(Materia, pk=materia_id)
        tema = request.POST.get('tema', False)
        if tema == False:
            return render(request, 'questions/temaVacio.html', {'materia': materia})
        preguntas = Question.objects.filter(nombre_materia=materia).filter(nombre_tema=tema)
        return render(request, 'questions/listaPreg.html', {'preguntas': preguntas})
    materia = get_object_or_404(Materia, pk=materia_id)
    temas = Tema.objects.filter(temas=materia)
    return render(request, 'questions/buscarT.html', {'materia': materia, 'temas': temas})


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
    return render(request, 'questions/modifiResp.html',{'answer': answer, 'question': question})


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
            guardarResp(q, opciones[x])
            if opciones[x] == "":
                q.delete()
                return render(request, 'questions/PregVacio.html')
    respuestas = Answer.objects.filter(respuesta=q)
    return render(request, 'questions/modificado.html', {'pregunta': q, 'respuestas': respuestas})


def reported(request):
    """
    Esta función redirecciona la vista a un html pasandole sólo las preguntas
    que estén reportadas.
    :Param request: HttpRequest
    :type: Http
    :Return: redirecciona a Http
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
    if request.method == "POST":
        question = get_object_or_404(Question, pk=question_id)
        answer = get_object_or_404(Answer, pk=answer_id)
        resp_nueva = request.POST['new_answer']
        answer.text_resp = resp_nueva
        answer.save()
        return render(request, 'questions/detail.html',
                      {'answers': Answer.objects.filter(respuesta=question),
                       'question': question})
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, pk=answer_id)
    return render(request, 'questions/update.html',
                  {'answer': answer,
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
