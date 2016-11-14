from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from examenes.models import Exam
from materias.models import Materia
from estadisticas.views import *

class EstadisticasTest(TestCase):

    def setUp(self):
        materia1 = Materia.objects.create(nombre_materia='Algebra')
        materia2 = Materia.objects.create(nombre_materia='Lengua')
        materia3 = Materia.objects.create(nombre_materia='Biologia')
        examen1 = Exam.objects.create(nombre_materia = 'Lengua',
                    nombre_tema = 'Lectura', cantidad_preg = 3,
                    tiempo_preg = 14, preguntas_correctas = 2,
                    preguntas_incorrectas = 1)
        examen4 = Exam.objects.create(nombre_materia = 'Lengua',
                    nombre_tema = 'Escritura', cantidad_preg = 6,
                    tiempo_preg = 14, preguntas_correctas = 4,
                    preguntas_incorrectas = 2)
        examen2 = Exam.objects.create(nombre_materia = 'Algebra',
                    nombre_tema = 'Matrices', cantidad_preg = 5,
                    tiempo_preg = 10, preguntas_correctas = 2,
                    preguntas_incorrectas = 3)
        examen3 = Exam.objects.create(nombre_materia = 'Algebra',
                    nombre_tema = 'Combinatoria', cantidad_preg = 4,
                    tiempo_preg = 9, preguntas_correctas = 2,
                    preguntas_incorrectas = 2)

    def test_lista_materias(self):
        response = self.client.get(reverse('estadisticas'))
        #print response
        self.assertEqual(response.resolver_match.func, estadistica_view)

    def test_estadistica_materia(self):
        materia = Materia.objects.get(nombre_materia='Lengua')
        response = self.client.get(reverse('estadis', args=[materia]))
        #print response
        self.assertEqual(response.resolver_match.func, estadis)

    def test_(self):
        pass