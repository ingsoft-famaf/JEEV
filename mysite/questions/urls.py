from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
<<<<<<< HEAD
    url(r'^$', views.question_view, name='uploadquestion'),
=======
    url(r'^$', views.upload_file, name='upload_question'),
>>>>>>> 4f124224b1e4add06f3127e040616bf1203855e7

    url(r'reported/', views.reported, name='reported'),

    url(r'^(?P<question_id>[0-9]+)/detail', views.detail_view,
        name='detail'),

    url(r'^(?P<question_id>[0-9]+)/delete', views.delete_view,
        name='delete'),

    url(r'^(?P<question_id>[0-9]+)/(?P<answer_id>[0-9]+)/update',
        views.update_view, name='update'),

    url(r'^(?P<question_id>[0-9]+)/(?P<answer_id>[0-9]+)/save',
        views.save_view, name='save'),

    url(r'^(?P<question_id>[0-9]+)/sacar', views.sacardereported,
        name='sacar'),
]
