from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


<<<<<<< HEAD
def homepage(request):
    return render(request, 'homepage/profile.html', {})

def profile_view(request):
    return render(request, 'users/profile.html', {})
=======
def index(request):
    return render_to_response('homepage/index.html')
>>>>>>> 575101d26b82737f78411a7265728a4f2e228985
