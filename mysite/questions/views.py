from django.shortcuts import render
from lxml import etree
from StringIO import StringIO
from lxml.builder import ElementMaker
from models import Question
# Create your views here.

#@login_required
#@permission_required('is_superuser')

class question_view():
    URL_TO_PARSE = '/home/usuario/Escritorio/XML/preg.xml'
    # URL_TO_PARSE=
    # '/home/usuario/Escritorio/Ingenieria/JEEV/static/Exams/preg.xml'
    URL = StringIO(URL_TO_PARSE)
    tree = etree.parse(URL_TO_PARSE)
    root = tree.getroot()
    child = root.getchildren()
    print(child)
    print ('feo')
    """E = ElementMaker()
    ROOT = E.root
    DOC = E.doc
    TEMA = E.field1
    SUBTEMA = E.field2
    MATERIA = E.field3
    VALOR = E.field4
    NUMERO = E.field5 
    the_doc = ROOT(
    				DOC(
    					TEMA("%s"(NombreTema), nombre='tema'),
    					SUBTEMA("%s"(NombreSubtema), nombre='subtema'),
    					MATERIA("%s"(NombreMateria), nombre ='materia'),
    				)
			)"""