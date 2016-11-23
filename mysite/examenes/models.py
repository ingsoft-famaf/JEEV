from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from questions.models import Question
import ast
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
    question = models.ForeignKey('questions.Question',
                                #on_delete=models.PROTECT,
                                blank=True, null=True)

    
class ExamErrores(models.Model):
    """
    Esta clase crea el modelo de examen, el examen va a tener como
    objetos el nombre de la materia, el nombre del tema, el tiempo para cada
    pregunta y la cantidad de preguntas a realizar.
    """
    nombre_materia = models.CharField(max_length=100)
    tiempo_preg = models.IntegerField(default=0)
    cantidad_preg = models.IntegerField(default=0)
    pregunta_actual = models.IntegerField(default=0)
    preguntas_correctas = models.IntegerField(default=0)
    preguntas_incorrectas = models.IntegerField(default=0)

class TemaE(models.Model):
    tema_fk = models.ForeignKey('ExamErrores', on_delete=models.CASCADE)
    nombre_tema = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_tema
        


class PregRespE(models.Model):
    examen = models.ForeignKey('ExamErrores', on_delete=models.CASCADE)
    question = models.ForeignKey('questions.Question',
                                #on_delete=models.PROTECT,
                                blank=True, null=True)


