from __future__ import unicode_literals

from django.db import models

class Homepage(models.Model):
    loguin_text = models.CharField(max_length=200)
    registro_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
