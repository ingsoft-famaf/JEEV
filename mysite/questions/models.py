from __future__ import unicode_literals
from xml import etree
from lxml.builder import ElementMaker
from django.db import models
# Create your models here.


class Question(models.Model):
	NombreTema = models.CharField(max_length=50)
	NombreSubtema = models.CharField(max_length=50)
	NombreMateria = models.CharField(max_length=50)
	NumeroPreg = models.IntegerField()
	ValorPreg = models.IntegerField()
	TextPreg = models.CharField(max_length=200)

"""
	E = ElementMaker()
	ROOT = E.root
	DOC = E.doc
	TEMA = E.field1
	SUBTEMA = E.field6
	FIELD2 = E.field2
	MATERIA = E.field3
	VALOR = E.field4
	NUMERO = E.field5

	the_doc = ROOT(
    				DOC(
        				TEMA("%s" % (NombreTema), name = 'tema'),
        				SUBTEMA("%s" % (NombreSubtema), name = 'subtema'),

    				)

				)


#E.TD("%s %s" % (row_num, col_num)) for col_num in range(3)R"""
