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
        response = self.client.post(
                reverse('cargarm'),
                data={
                    'nueva_materia': 'Quimica'})
        self.assertEqual(response.resolver_match.func, cargarm)

class TemaMethodTests(TestCase):

    def test_se_cargo_tema_correctamente(self):
        pass