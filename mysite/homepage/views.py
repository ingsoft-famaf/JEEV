from django.http import HttpResponse
from django.shortcuts import render
from questions.models import Question


def homepage(request):
    return render(request, 'homepage/homepage.html',
                  {'list_reported': Question.objects.filter(reportada=True)})

def superuser_view(request):
    return render(request, 'homepage/superuser.html', {})


