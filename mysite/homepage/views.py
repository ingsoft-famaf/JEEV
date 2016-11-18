from django.http import HttpResponse
from django.shortcuts import render
from questions.models import Question


def homepage(request):
    """ Esta def te redirijira al inicio o home, usando el logueo de
    un usuario.
    :Param request: HttpRequest
    :Type: metodo
    :return:redirecciona al homepage.html

    """
    return render(request, 'homepage/homepage.html',
                  {'list_reported': Question.objects.filter(reportada=True)})


def superuser_view(request):
    """ Esta def te redirijira al inicio o home del admin, usando el logueo de
    un administrador. Esta debera tener un menu diferente al del usuario comun.
    :Param request: HttpRequest
    :Type: metodo
    :return:redirecciona al superuser.html
    """
    return render(request, 'homepage/superuser.html', {})
