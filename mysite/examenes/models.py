from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from questions.models import Question
#from djangotoolbox.fields import ListField

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
    pregunta_actual = models.IntegerField(default=0)
    preguntas_correctas = models.IntegerField(default=0)
    preguntas_incorrectas = models.IntegerField(default=0)

class PregResp(models.Model):
    examen = models.ForeignKey('Exam', on_delete=models.CASCADE)
    question_id = models.CharField(max_length=100)

class ExamErrores(models.Model):
    """
    Esta clase crea el modelo de examen basado en errores, el examen va a tener
    como objetos el nombre de la materia, el nombre del tema, el tiempo para
    cada pregunta y la cantidad de preguntas a realizar.
    """
    nombre_materia = models.CharField(max_length=100)
    cantidad_temas = models.IntegerField(default=0)
    nombre_tema = models.CharField(max_length=100)
    tiempo_preg = models.IntegerField(default=0)
    cantidad_preg = models.IntegerField(default=0)
    pregunta_actual = models.IntegerField(default=0)
    preguntas_correctas = models.IntegerField(default=0)
    preguntas_incorrectas = models.IntegerField(default=0)