from django.test import TestCase
from questions.models import Question

# Create your tests here.


class UploadQuestionTest(TestCase):

	def __init__(self):
		quiestion_view('/home/usuario/Escritorio/XML/preg.xml')		

	def test_verify_upload(self):
		question = Question.object.get(materia="Alegra")
		materia = question.find('materia').text
        #tema = question.find('tema').text
        #texto = question.find('texto').text
        self.assertEqual(materia, 'Algebra')
        #self.assertEqual(tema, 'matrices')
        #self.assertEqual(text, 'Esta matriz es inversible?')