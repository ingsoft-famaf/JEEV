from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class Question(models.Model):
    """
    Esta clase crea el modelo de las preguntas, las preguntas van a tener como
    objetos el nombre de la materia, el nombre del tema, el texto de la
    pregunta y un campo booleano donde indica si esta reportada o no.
    """
    nombre_tema = models.CharField(max_length=100)
    nombre_materia = models.CharField(max_length=100)
    text_preg = models.CharField(max_length=200)
    reportada = models.BooleanField(default=False)
    nota_reporte = models.CharField(max_length=200)

    def __str__(self):
        return self.text_preg


class Answer(models.Model):
    """
    Esta clase crea el modelo de las respuestas. Las respuestas van a estar
    relacionadas con la pregunta correspondiente, van a tener como objetos
    el texto de la respuesta y un campo booleano donde indica si es la
    correcta o no.
    """
    respuesta = models.ForeignKey('Question', on_delete=models.CASCADE)
    text_resp = models.CharField(max_length=500)
    es_correcta = models.BooleanField(default=False)
