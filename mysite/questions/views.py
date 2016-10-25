from django.shortcuts import render
from lxml import etree
from StringIO import StringIO
from lxml.builder import ElementMaker
from models import Question
# Create your views here.

#@login_required
#@permission_required('is_superuser')


class question_view():
    

    def get_distancia(str1,str2):
        d=dict()
        for i in range(len(str1)+1):
            d[i]=dict()
            d[i][0]=i
        for i in range(len(str2)+1):
            d[0][i] = i
        for i in range(1, len(str1)+1):
            for j in range(1, len(str2)+1):
                d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
        return d[len(str1)][len(str2)]


    URL_TO_PARSE = '/home/usuario/Escritorio/XML/preg.xml'
    URL = StringIO(URL_TO_PARSE)
    tree = etree.parse(URL_TO_PARSE)
    root = tree.getroot()
    for pregunta in root:
        materia = pregunta.find('materia').text
        tema = pregunta.find('tema').text
        texto = pregunta.find('texto').text
        # print type(tema)
        print materia
        print tema
        # q = Question(NombreTema=tema,NombreMateria = materia,TextPreg=texto)
        # q.save()
        query = Question.objects.filter(
            NombreTema=tema).filter(NombreMateria=materia)

        count = query.count()
        print ('el conteo de preguntas con mismo tema y materia: %s' % count)
        if count == 0:
            #q = Question(NombreTema=tema,NombreMateria = materia,TextPreg=texto)
            #q.save()
            print('Pregunta creada')
        else:
             for i in range(count):
                print ('la i en el bucle es %s' % i)
                firstObj = query[i]
                print firstObj.TextPreg
                print texto
                print ('la distancia es %s' % get_distancia(firstObj.TextPreg,texto))
                if get_distancia(firstObj.TextPreg,texto) == 0:
                    print('pregunta repetida')
                else:
                    #q = Question(NombreTema=tema,NombreMateria = materia,TextPreg=texto)
                    #q.save()
                    print('pregunta creada 2')
    #all_objects = Question.objects.all().delete()
    # qobject = Question.objects.get(NombreTema= tema)
    # print qobject.NombreMateria
    # print(root[1][0].text)
    """
            for i in range(count):
                firstObj = query[i]
                print firstObj.TextPreg
    """
    print('feo')