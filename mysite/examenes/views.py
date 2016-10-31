from django.http import HttpResponse
from django.shortcuts import render

def examenperfil(request):
    print ("hola")
    return render(request, 'examenes/examenperfil.html', {})
