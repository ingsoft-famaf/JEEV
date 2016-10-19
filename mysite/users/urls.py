from django.shortcuts import render
from django.conf.urls import url
from allauth.account.views import SignupView

urlpatterns = [
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^signup/', SignupView, name='account_signup'),
    url(r'^profile/', views.profile_view, name='profile'),
]
