from django.http import HttpResponse
from django.shortcuts import render

def cargarmateria(request):
    return render(request, 'materias/cargarmateria.html', {})

def cargartema(request):
    return render(request, 'materias/cargartema.html', {})
