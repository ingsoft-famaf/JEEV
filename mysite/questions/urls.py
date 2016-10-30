from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.question_view, name='question'),
    url(r'^reported', views.reported_view, name='reported'),
    url(r'^(?P<question_id>[0-9]+)/detail', views.detail_view,
        name='detail'),
    url(r'^(?P<question_id>[0-9]+)/delete', views.delete_view,
        name='delete'),
    url(r'^(?P<question_id>[0-9]+)/(?P<answer_id>[0-9]+)/update',
        views.update_view, name='update'),
    url(r'^(?P<question_id>[0-9]+)/(?P<answer_id>[0-9]+)/save',
        views.save_view, name='save'),
]
