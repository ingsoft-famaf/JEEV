from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from examenes.models import Exam
from materias.models import Materia
from django.db.models import Avg, Sum, FloatField
import scipy as sp
from matplotlib import pyplot
import matplotlib.pyplot as plt


def grafico(request, materia):
        # Creamos el array x de cero a cien con cien puntos
    #x = sp.linspace(0, 10, 100)
    # Creamos el array y conde cada punto es el seno de cada elemento de x
    #y = sp.sin(x)
    # Creamos una figura
    #plt.figure()
    lista_examenes = Exam.objects.filter(nombre_materia=materia)
    porcentajes = []
    for x in xrange(lista_examenes.count()):
        nota = lista_examenes[x].preguntas_correctas
        nota1 = lista_examenes[x].cantidad_preg
        porcentajes.append((nota * 100)/ nota1)
    # Representamos
    y = porcentajes
    listx = []
    for x in xrange(1,lista_examenes.count()+1):
        listx.append(x)
    print listx
    plt.plot(listx,y)
    #plt.title('Grafico de %s', )
    plt.xlabel('tiempo en dias')
    plt.ylabel('porcentaje')

    # Mostramos en pantalla
    plt.show()


def estadistica_view(request):
    if request.method == "POST":
        materia = request.POST['materia']
        lista_examenes = Exam.objects.filter(nombre_materia=materia)
        cant_preguntas = lista_examenes.aggregate(Sum('cantidad_preg'))
        preg_correctas = lista_examenes.aggregate(Sum('preguntas_correctas'))
        preg_incorrectas = lista_examenes.aggregate(Sum('preguntas_incorrectas'))
        promedio = lista_examenes.aggregate(Avg('preguntas_correctas'))
        promedio= (promedio['preguntas_correctas__avg'])*10
        return render(request, 'estadisticas/general.html',
                      {'lista_examenes': lista_examenes, 'cant_preguntas': cant_preguntas,
                       'preg_correctas':preg_correctas, 'preg_incorrectas': preg_incorrectas,
                       'materia': materia, 'promedio': promedio})
    lista_materias = Exam.objects.values_list(
                            'nombre_materia', flat=True).distinct()

    for x in xrange(lista_materias.count()):
        """
        lista_examenes = Exam.objects.filter(nombre_materia=lista_materias[x])
        promedios.append(lista_examenes.aggregate(Avg('preguntas_correctas')))
        print promedios[x]
        """
        lista_examenes = Exam.objects.filter(nombre_materia=lista_materias[x])
        promedio = lista_examenes.aggregate(Avg('preguntas_correctas'))
        materia = get_object_or_404(Materia, nombre_materia=lista_materias[x])
        materia.promedio = (promedio['preguntas_correctas__avg'])*10
        materia.save()
    materias = Materia.objects.all()
    return render(request, 'estadisticas/estadis.html',
                  {'materias': materias})


def estadis_examen(request, examen_id):
    examen = get_object_or_404(Exam, pk=examen_id)
    nota = examen.preguntas_correctas
    nota1 = examen.cantidad_preg
    nota = (nota * 100)/ nota1
    return render(request, 'estadisticas/estadisExamen.html',
                  {'examen': examen, 'nota': nota})