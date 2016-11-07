from django.test import TestCase

from .models import Materia, Tema

class MateriaMethodTests(TestCase):
    """
    Este test debería devolver true si la materia se cargó
    correctamente.
    NO se cargó materia en blanco.
    No se cargó matería que ya existe.
    """
	def test_se_cargo_materia_correctamente(self):
	     self.assertIs(future_question.was_published_recently(), False)

class TemaMethodTests(TestCase):
	"""
	Si se cargó correctamente el tema.
	Si no se cargó repetido el tema
	Si no se cargó tema en blanco
	"""
	def test_se_cargo_tema_correctamente(self):