from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    return render(request, 'homepage/profile.html', {})

def profile_view(request):
    return render(request, 'users/profile.html', {})

def superuser_view(request):
    return render(request, 'homepage/superuser.html', {})

def index_view(request):
    return render(request, 'homepage/index.html', {})




