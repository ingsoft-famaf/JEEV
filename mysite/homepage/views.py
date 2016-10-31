from django.http import HttpResponse
from django.shortcuts import render



def homepage(request):
    return render(request, 'homepage/homepage.html', {})

def superuser_view(request):
    return render(request, 'homepage/superuser.html', {})


