from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    return render(request, 'homepage/profile.html', {})

def profile_view(request):
    return render(request, 'users/profile.html', {})
