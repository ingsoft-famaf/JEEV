# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client

from .models import Materia, Tema

class MateriaMethodTests(TestCase):

    def test_se_cargo_materia_correctamente(self):
        response = self.client.post(
                reverse('cargarm'),
                data={
                    'nueva_materia': 'casa'})
        print response
        self.assertRedirects(response, '/materias/secargo/') 

class TemaMethodTests(TestCase):

    def test_se_cargo_tema_correctamente(self):
        pass