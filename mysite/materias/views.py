# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from models import Materia


def cargarmateria(request):
    nuevamateria = request.POST['nueva_materia']
    m = Materia(nombre_materia=nuevamateria)
    m.save()
    return HttpResponse('se cargo la materia con exito!')

def cargartema(request):
    return render(request, 'materias/cargartema.html', {})
