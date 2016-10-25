from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Question(models.Model):
    NombreTema = models.CharField(max_length=100)
    NombreMateria = models.CharField(max_length=100)
    TextPreg = models.CharField(max_length=200)
    Reportada = models.BooleanField(default=False)

    def __str__(self):
        return self.TextPreg