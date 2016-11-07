from django.shortcuts import render, get_object_or_404
from examenes.models import Exam


def estadistica_view(request):
    if request.method == "POST":
        materia = request.POST['materia']
        lista_examenes = Exam.objects.filter(nombre_materia=materia)
        cant_preguntas = lista_examenes.values('cantidad_preg')
        preg_correctas = lista_examenes.values_list(
                                'preguntas_correctas', flat = True).distinct()
        preg_incorrectas = lista_examenes.values_list(
                                'preguntas_incorrectas', flat = True).distinct()
        for x in xrange(1,cant_preguntas.count()):
            print cant_preguntas[x]
        print cant_preguntas
        print preg_correctas
        print preg_incorrectas
        return render(request, 'estadisticas/general.html',
                      {'lista_examenes': lista_examenes, 'cant_preguntas': cant_preguntas,
                       'preg_correctas':preg_correctas, 'preg_incorrectas': preg_incorrectas,
                       'materia': materia})
    return render(request, 'estadisticas/estadis.html',
                  {'materias': Exam.objects.values_list(
                               'nombre_materia', flat=True).distinct()})
