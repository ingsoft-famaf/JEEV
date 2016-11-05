# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from models import Materia, Tema


def cargarm(request):
    if request.method == "POST":
        nuevamat = request.POST['nueva_materia']
        m = Materia(nombre_materia=nuevamat)
        m.save()
        return render(request, 'materias/secargo.html')
    return render(request, 'materias/cargarmateria.html')


def cargart(request):
    if request.method == "POST":
        materia = request.POST['materias']
        nuevotema = request.POST['nuevo_tema']
        mt = Materia.objects.filter(nombre_materia = materia)
        print mt
        m = Tema(temas= Materia.objects.filter(nombre_materia = materia), nombre_tema=nuevotema)
        print m
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

