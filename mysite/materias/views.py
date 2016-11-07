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
    if request.method == "POST":
        nuevamat = request.POST['nueva_materia']
        query = Materia.objects.filter(nombre_materia=nuevamat)
        count = query.count()       
        if count == 0:
            q = Materia(nombre_materia=nuevamat)
            q.save()
        else:
            for i in range(count):
                repetida = False
                firstObj = query[i]
                print type(firstObj.nombre_materia)
                print type(nuevamat)
                if distance(str(firstObj.nombre_materia), str(nuevamat)) == 0:
                    repetida = True
                    return render(request, 'materias/repetida.html')
                 #   break
            if repetida is False:
                q = Materia(nombre_materia=nuevamat)
                q.save()
        return render(request, 'materias/secargo.html')
    return render(request, 'materias/cargarmateria.html')


def cargart(request):
    if request.method == "POST" and request.method != "NULL":
            materia = request.POST['materias']
            nuevotema = request.POST['nuevo_tema']
            mt = Materia.objects.filter(nombre_materia = materia)
            print mt
            query = Tema.objects.filter(nombre_tema=nuevotema)
            count = query.count()       
            if count == 0:
                m = Tema(temas= mt[0], nombre_tema=nuevotema)
                m.save()
            else:
                for i in range(count):
                    repetida = False
                    firstObj = query[i]
                    if distance(str(firstObj.nombre_tema), str(nuevotema)) == 0:
                        repetida = True
                        return render(request, 'materias/temarepetido.html')
                     #   break
                if repetida is False:
                    m = Tema(temas= mt[0], nombre_tema=nuevotema)
                    m.save()
            return render(request, 'materias/secargo.html')
    return render(request, 'materias/cargartema.html',{'list_materias': Materia.objects.values_list(
                        'nombre_materia', flat=True).distinct()})

def obtener_tema_materia(request):
    print "hola"
    print (Materia.objects.values_list(
                            'nombre_materia', flat=True))
    return render(request, 'materias/cargartema.html',
              {'list_materias': Materia.objects.values_list(
                        'nombre_materia', flat=True).distinct()})

