from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^(?P<question_id>[0-9]+)/guardarCorrecta', views.guardarCorrecta, name='guardarCorrecta'),
    url(r'^agregarPreg', views.agregarPreg, name='agregarPreg'),
    url(r'^uploadquestion', views.uploadquestion, name='uploadquestion'),
    url(r'reported/', views.reported, name='reported'),
    url(r'^(?P<question_id>[0-9]+)/detail', views.detail_view, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/delete', views.delete_view, name='delete'),
    url(r'^(?P<question_id>[0-9]+)/(?P<answer_id>[0-9]+)/update', views.update_view, name='update'),
    url(r'^(?P<question_id>[0-9]+)/(?P<answer_id>[0-9]+)/save', views.save_view, name='save'),
    url(r'^(?P<question_id>[0-9]+)/sacar', views.sacardereported, name='sacar'),
]
