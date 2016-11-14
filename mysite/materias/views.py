# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from models import Materia, Tema
from Levenshtein import *


# Las tres funciones de esta view toman HttpRequest como su primer parámetro y
# devuelven una instancia de HttpResponse utilizando el atajo render.
# Los parámetros de render son request y template_name.


# cargarm 
def cargarm(request):
    """ :Param request: HttpRequest
        :type: Http
        :return: redirecciona a Http segun corresponda el caso """
    if request.method == "POST":
        nuevamat = request.POST['nueva_materia']
	if nuevamat == "" or nuevamat == " ":
		return render(request, 'materias/repetida.html')
        if type(nuevamat) != unicode:
            return render(request, 'materias/repetida.html')
        query = Materia.objects.filter(nombre_materia=nuevamat)
        count = query.count()       
        if count == 0:
            nmat = Materia(nombre_materia=nuevamat)
            nmat.save()
        else:
            repetida = False
            nmat = Materia(nombre_materia=nuevamat)
            if distance(str(nmat), str(nuevamat)) <= 0:
                repetida = True
            if repetida is False:
                nmat = Materia(nombre_materia=nuevamat)
                nmat.save()
            else:
                return render(request, 'materias/repetida.html')
    	return render(request, 'materias/secargo.html')
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
    print (Materia.objects.values_list(
                            'nombre_materia', flat=True))
    return render(request, 'materias/cargartema.html',
              {'list_materias': Materia.objects.values_list(
                                'nombre_materia', flat=True).distinct()})
