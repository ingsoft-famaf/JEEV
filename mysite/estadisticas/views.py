from django.shortcuts import render, get_object_or_404
from examenes.models import Exam
from django.db.models import Avg, Sum, FloatField


def estadistica_view(request):
    if request.method == "POST":
        materia = request.POST['materia']
        lista_examenes = Exam.objects.filter(nombre_materia=materia)
        cant_preguntas = lista_examenes.aggregate(Sum('cantidad_preg'))
        preg_correctas = lista_examenes.aggregate(Sum('preguntas_correctas'))
        preg_incorrectas =
        lista_examenes.aggregate(Sum('preguntas_incorrectas'))
        promedio = lista_examenes.aggregate(Avg('preguntas_correctas'))
        return render(request, 'estadisticas/general.html',
                        {'lista_examenes': lista_examenes,
                        'cant_preguntas': cant_preguntas,
                        'preg_correctas': preg_correctas,
                        'preg_incorrectas': preg_incorrectas,
                        'materia': materia, 'promedio': promedio})
    return render(request, 'estadisticas/estadis.html',
                  {'materias': Exam.objects.values_list(
                               'nombre_materia', flat=True).distinct()})
