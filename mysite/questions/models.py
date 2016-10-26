from __future__ import unicode_literals
from xml import etree
from lxml.builder import ElementMaker
from django.db import models
# Create your models here.


class Question(models.Model):
    NombreTema = models.CharField(max_length=100)
    NombreMateria = models.CharField(max_length=100)
    TextPreg = models.CharField(max_length=200)


class Answer(models.Model):
	respuesta = models.ForeignKey('Question', on_delete=models.CASCADE)
	text_resp = models.CharField(max_length=500)
	es_correcta = models.BooleanField(default=False)
