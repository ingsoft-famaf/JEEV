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
        nuevotema = request.POST['nuevo_tema']
        m = Tema(nombre_tema=nuevotema)
        m.save()
        return render(request, 'materias/secargo.html')
    return render(request, 'materias/cargartema.html')
