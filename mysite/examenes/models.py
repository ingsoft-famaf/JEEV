from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class Exam(models.Model):
    """
    Esta clase crea el modelo de examen, el examen va a tener como
    objetos el nombre de la materia, el nombre del tema, el tiempo para cada
    pregunta y la cantidad de preguntas a realizar.
    """
    nombre_tema = models.CharField(max_length=100)
    nombre_materia = models.CharField(max_length=100)
    tiempo_preg = models.IntegerField(default=0)
    cantidad_preg = models.IntegerField(default=0)
    #preg_list = models.questions()
