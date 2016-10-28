from __future__ import unicode_literals
from xml import etree
from lxml.builder import ElementMaker
from django.db import models
# Create your models here.


class Question(models.Model):
    nombre_tema = models.CharField(max_length=100)
    nombre_materia = models.CharField(max_length=100)
    text_preg = models.CharField(max_length=200)
    
    def __str__(self):
        return self.text_preg

class Answer(models.Model):
	respuesta = models.ForeignKey('Question', on_delete=models.CASCADE)
	text_resp = models.CharField(max_length=500)
	es_correcta = models.BooleanField(default=False)
