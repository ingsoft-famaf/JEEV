from django.shortcuts import render
from django.conf.urls import url

from . import views

urlpatterns = [
<<<<<<< HEAD
    url(r'^', views.homepage, name='profile'),
    #url(r'^$', views.index, name='index'),
=======
    url(r'^$', views.index, name='index'),
#    url(r'^$', views.DetailView.as_view(), name='detail'),
>>>>>>> 575101d26b82737f78411a7265728a4f2e228985
]
