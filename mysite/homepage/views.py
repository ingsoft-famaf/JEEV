from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    return render(request, 'homepage/homepage.html', {})

def profile_view(request):
    return render(request, 'users/profile.html', {})

def superuser_view(request):
    return render(request, 'homepage/superuser.html', {})

def indexadmin_view(request):
    return render(request, 'homepage/indexadmin.html', {})




