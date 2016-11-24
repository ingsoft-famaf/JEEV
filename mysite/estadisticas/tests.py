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
        examen1 = Exam.objects.create(nombre_materia='Lengua', cantidad_preg=3,
                                      tiempo_preg=14, preguntas_correctas=2, preguntas_incorrectas=1)
        examen2 = Exam.objects.create(nombre_materia='Lengua', cantidad_preg=6,
                                      tiempo_preg=14, preguntas_correctas=4, preguntas_incorrectas=2)
        examen3 = Exam.objects.create(nombre_materia='Algebra', cantidad_preg=5,
                                      tiempo_preg=10, preguntas_correctas=2, preguntas_incorrectas=3)

    def test_lista_materias(self):
        """el usuario se redirecciona a estadisticas para observar las
            estadisticas de su historial.
            precondicion: simula ingresar pedido de redireccion.
            post : compara si el resultado es la pagina con toda la estadisticas.
        """
        response = self.client.get(reverse('estadisticas'))
        self.assertEqual(response.resolver_match.func, estadistica_view)

    def test_estadistica_materia(self):
        """simula pedir el nombre de la materia lenguas
            pre: se redirecciona a estadis con el arg materia.
            post: compara el resultado si es igual al esperado
        """
        materia = Materia.objects.get(nombre_materia='Lengua')
        response = self.client.get(reverse('estadis', args=[materia]))
        self.assertEqual(response.resolver_match.func, estadis)

    def test_estadistica_examen(self):
        materia = Materia.objects.get(nombre_materia='Algebra')
        response = self.client.get(reverse('estadis', args=[materia]))
        examen = Exam.objects.get(pk=3)
        response1 = self.client.get(reverse('estadis_examen', args=[examen.id]))
        self.assertEqual(response1.resolver_match.func, estadis_examen)
