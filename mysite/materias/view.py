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
    if nuevamat == "" or nuevamat == " ":
        return render(request, 'materias/repetida.html')
#        if type(nuevamat) != unicode:
  #          return render(request, 'materias/repetida.html')
        query = Materia.objects.filter(nombre_materia__iexact=nuevamat)
        print query
        print nuevamat
        print "no entro if"
        repetida = False
        count = query.count()
        q = Materia(nombre_materia=nuevamat)
        if count != 0:
            if distance(str(Materia.objects.filter(nombre_materia=nuevamat)), str(nuevamat)) <= 0:
                repetida = True
                print "entro if distancia"
            if repetida is False:
                q = Materia(nombre_materia=nuevamat)
                q.save()
                print "no repetida"
            else:
                print "repetida"
                return render(request, 'materias/repetida.html')
        else:
            q.save()
            print "guardo igual"
            return render(request, 'materias/secargo.html')
    return render(request, 'materias/cargarmateria.html')


def cargart(request):
    if request.method == "POST":
        materia = request.POST['materias']
        nuevotema = request.POST['nuevo_tema']
    if nuevotema == "" or nuevotema == " ":
        return render(request, 'materias/temarepetido.html')
    else:
            mat = Materia.objects.filter(nombre_materia = materia)
        print mat
        query = Tema.objects.filter(nombre_tema=nuevotema)
        count = query.count()       
        if count == 0:
            ntema = Tema(temas= mat[0], nombre_tema=nuevotema)
            ntema.save()
        else:
            repetida = False
            ntema = Tema(temas= mat[0], nombre_tema=nuevotema)
            if distance(str(ntema), str(nuevotema)) <= 0:
                repetida = True
            if repetida is False:
                ntema = Tema(temas= mat[0], nombre_tema=nuevotema)
                ntema.save()
            else:
               return render(request, 'materias/temarepetido.html')
        return render(request, 'materias/secargo.html')
    return render(request, 'materias/cargartema.html',{'list_materias': Materia.objects.values_list(
                        'nombre_materia', flat=True).distinct()})

def obtener_tema_materia(request):
    print (Materia.objects.values_list(
                            'nombre_materia', flat=True))
    return render(request, 'materias/cargartema.html',
              {'list_materias': Materia.objects.values_list(
                        'nombre_materia', flat=True).distinct()})

