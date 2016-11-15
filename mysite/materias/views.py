# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from models import Materia, Tema
from Levenshtein import *

def cargarm(request):
    """ :Param request: HttpRequest
        :type: Http
        :return: redirecciona a Http segun corresponda el caso """
    if request.method == "POST":
        nuevamat = request.POST['nueva_materia']
        if nuevamat == "" or nuevamat == " ":
            return render(request, 'materias/repetida.html')
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
        :return: redirecciona a Http segun corresponda el caso """
    
    if request.method == "POST":
        materia = request.POST['materias']
        nuevotema = request.POST['nuevo_tema']
        if nuevotema == "" or nuevotema == " ":
            return render(request, 'materias/temarepetido.html')
        mat = Materia.objects.filter(nombre_materia = materia)
        query = Tema.objects.filter(nombre_tema__iexact=nuevotema)
        repetida = False
        count = query.count()
        ntema = Tema(temas= mat[0], nombre_tema=nuevotema)
        if count == 0:
            ntema.save()
            return render(request, 'materias/secargo.html')
        else:
            if distance(str(query[0]).lower(), str(nuevotema).lower()) == 0:
                repetida = True
            if repetida is False:
                ntema = Tema(temas= mat[0], nombre_tema=nuevotema)
                ntema.save()
                return render(request, 'materias/secargo.html')
            else:
               return render(request, 'materias/temarepetido.html')
    return render(request, 'materias/cargartema.html',{'list_materias': Materia.objects.values_list(
                        'nombre_materia', flat=True).distinct()})


def obtener_tema_materia(request):
    """:Param request: HttpRequest
    :type: Http
    :return: redirecciona a Http segun corresponda """
    #print (Materia.objects.values_list(
    #                        'nombre_materia', flat=True))
    return render(request, 'materias/cargartema.html',
              {'list_materias': Materia.objects.values_list(
                                'nombre_materia', flat=True).distinct()})
