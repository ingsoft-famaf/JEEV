from __future__ import unicode_literals
from django.db import models


class Materia(models.Model):
    """
    Crea una tabla con el campo nombre_materia
    :param models: modelo o estructura de base de datos
    :type: Model
    """
    nombre_materia = models.CharField(max_length=100)
    promedio = models.FloatField(default=0)

    def __str__(self):
        return self.nombre_materia


class Tema(models.Model):
    """
    Crea una tabla con el campo temas y nombre de temas
    :param models: modelo o estructura de base de datos
    :type: Model
    """
    temas = models.ForeignKey('Materia', on_delete=models.CASCADE)
    nombre_tema = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_tema
