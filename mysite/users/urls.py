from django.shortcuts import render
from django.conf.urls import url
from allauth.account.views import SignupView, LogoutView
from django.contrib.auth.decorators import permission_required
from . import views

urlpatterns = [
    url(r'^logout/', LogoutView, name='account_logout'),
    url(r'^signup/', SignupView, name='account_signup'),
]
