from django.http import HttpResponse
from django.shortcuts import render
from models import Materia, Tema
from Levenshtein import *


def modificacion_input(string):
    """
    Esta funcion transfomar el string de input en un string sin espacios
    y con la primera letra en mayuscula
    :Param string: string
    :Return: String
    """
    string_splited = "".join(string.split())
    string_lower = string_splited.lower()
    string_titled = string_lower.title()
    return string_titled


def cargarm(request):
    """ :Param request: HttpRequest
        :type: Http
        :return: redirecciona a Http segun corresponda el caso
    """
    if request.method == "POST":
        nuevaM = request.POST['nueva_materia']
        nuevamat = modificacion_input(nuevaM)
        if nuevamat == "" or nuevamat == " ":
            return render(request, 'materias/vacio.html')
        query = Materia.objects.filter(nombre_materia__iexact=nuevamat)
        repetida = False
        count = query.count()
        q = Materia(nombre_materia=nuevamat)
        if count == 0:
            q.save()
            return render(request, 'materias/secargo.html')
        else:
            if distance(str(query[0]).lower(), str(nuevamat).lower()) == 0:
                repetida = True
            if repetida is False:
                q = Materia(nombre_materia=nuevamat)
                q.save()
                return render(request, 'materias/secargo.html')
            else:
                return render(request, 'materias/repetida.html')
    return render(request, 'materias/cargarmateria.html')


def cargart(request):
    """
        :Param request: HttpRequest
        :type: Http
        :return: redirecciona a Http segun corresponda el caso
    """
    if request.method == "POST":
        materia = request.POST['materias']
        nuevoT = request.POST['nuevo_tema']
        nuevotema = modificacion_input(nuevoT)
        if nuevotema == "" or nuevotema == " ":
            return render(request, 'materias/temavacio.html')
        mat = Materia.objects.filter(nombre_materia=materia)
        query = Tema.objects.filter(nombre_tema__iexact=nuevotema)
        repetida = False
        count = query.count()
        ntema = Tema(temas=mat[0], nombre_tema=nuevotema)
        if count == 0:
            ntema.save()
            return render(request, 'materias/secargo.html')
        else:
            if distance(str(query[0]).lower(), str(nuevotema).lower()) == 0:
                repetida = True
            if repetida is False:
                ntema = Tema(temas=mat[0], nombre_tema=nuevotema)
                ntema.save()
                return render(request, 'materias/secargo.html')
            else:
                return render(request, 'materias/temarepetido.html')
    return render(request, 'materias/cargartema.html', {'list_materias': Materia.objects.values_list(
                                                        'nombre_materia', flat=True).distinct()})


def obtener_tema_materia(request):
    """:Param request: HttpRequest
    :type: Http
    :return: redirecciona a Http segun corresponda
    """
    return render(request, 'materias/cargartema.html', {'list_materias': Materia.objects.values_list(
                                                        'nombre_materia', flat=True).distinct()})
