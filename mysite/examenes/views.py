from django.http import HttpResponse
from django.shortcuts import render

def examen_view(request):
    return render(request, 'examenes/examenPerfil.html', {})

