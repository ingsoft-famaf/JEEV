from __future__ import unicode_literals

from django.db import models


class Materia(models.Model):
    nombre_materia = models.CharField(max_length=30)


    def __str__(self):
        return self.nombre_materia


class Tema(models.Model):
    temas = models.ForeignKey('Materia', on_delete=models.CASCADE)
    nombre_tema = models.CharField(max_length=30)
   # materias = models.ManyToManyField(Materia)


    def __str__(self):
        return self.nombre_tema