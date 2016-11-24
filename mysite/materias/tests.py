# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from materias.views import *
from .models import Materia, Tema


class MateriaMethodTests(TestCase):

    def setUp(self):
        materia1 = Materia.objects.create(nombre_materia='Biologia')
        materia2 = Materia.objects.create(nombre_materia='Algebra')

    def test_se_cargo_materia_correctamente(self):
        """
        pre: carga datos y envia un formulario a la funcion cargrm
        post:
        """
        response = self.client.post(reverse('cargarm'), data={'nueva_materia': 'Quimica'})
        self.assertEqual(response.resolver_match.func, cargarm)

    def test_se_cargo_materia_repetida(self):
        response = self.client.post(reverse('cargarm'), data={'nueva_materia': 'Quimica'})
        response = self.client.post(reverse('cargarm'), data={'nueva_materia': 'Quimica'})
        self.assertEqual(response.resolver_match.func, cargarm)

    def test_se_cargo_materia_repetida2(self):
        response = self.client.post(reverse('cargarm'), data={'nueva_materia': 'Quimica'})
        response = self.client.post(reverse('cargarm'), data={'nueva_materia': 'quimica'})
        self.assertEqual(response.resolver_match.func, cargarm)

    def test_se_cargo_materia_vacia(self):
        response = self.client.post(reverse('cargarm'), data={'nueva_materia': ""})
        self.assertEqual(response.resolver_match.func, cargarm)

    def test_se_cargo_materia_vacia(self):
        response = self.client.post(reverse('cargarm'), data={'nueva_materia': " "})
        self.assertEqual(response.resolver_match.func, cargarm)


class TemaMethodTests(TestCase):

    def setUp(self):
        materia1 = Materia.objects.create(nombre_materia='Biologia')
        materia2 = Materia.objects.create(nombre_materia='Algebra')

    def test_se_cargo_tema_correctamente(self):
        response = self.client.post(reverse('cargart'),
                                    data={'materias': 'Biologia',
                                          'nuevo_tema': 'genetica'})
        self.assertEqual(response.resolver_match.func, cargart)

    def test_se_cargo_tema_repetido(self):
        response = self.client.post(reverse('cargart'),
                                    data={'materias': 'Biologia',
                                          'nuevo_tema': 'genetica'})
        response = self.client.post(reverse('cargart'),
                                    data={'materias': 'Biologia',
                                          'nuevo_tema': 'genetica'})
        self.assertEqual(response.resolver_match.func, cargart)

    def test_se_cargo_tema_vacio(self):
        response = self.client.post(reverse('cargart'),
                                    data={'materias': 'Algebra',
                                          'nuevo_tema': ""})
        response = self.client.post(reverse('cargart'),
                                    data={'materias': 'Algebra',
                                          'nuevo_tema': " "})
        self.assertEqual(response.resolver_match.func, cargart)
