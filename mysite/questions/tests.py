from django.test import TestCase
from django.core.urlresolvers import reverse
from allauth.account.forms import BaseSignupForm
from django.test.client import Client
from allauth.utils import get_user_model
from questions.models import Question, Answer
from examenes.views import *
from questions.views import *


class QuestionTest(TestCase):

    def setUp(self):

        question1 = Question.objects.create(nombre_tema='restar',
                                            nombre_materia='Matematicas',
                                            text_preg='3-2 ?',
                                            reportada=False)
        Answer.objects.create(respuesta=question1, text_resp='1',
                              es_correcta=True)
        Answer.objects.create(respuesta=question1, text_resp="0",
                              es_correcta=False)
        Answer.objects.create(respuesta=question1, text_resp="2",
                              es_correcta=False)
        question2 = Question.objects.create(nombre_tema='sumar',
                                            nombre_materia='Matematicas',
                                            text_preg='5 x 5 ?',
                                            reportada=False)
        Answer.objects.create(respuesta=question2, text_resp='25',
                              es_correcta=True)
        Answer.objects.create(respuesta=question2, text_resp="55",
                              es_correcta=False)
        Answer.objects.create(respuesta=question2, text_resp="26",
                              es_correcta=False)
        question3 = Question.objects.create(nombre_tema='Lectura',
                                            nombre_materia='Lengua',
                                            text_preg='frodo amigo de sam?',
                                            reportada=False)
        Answer.objects.create(respuesta=question1, text_resp='si',
                              es_correcta=True)
        Answer.objects.create(respuesta=question1, text_resp="no",
                              es_correcta=False)
        question4 = Question.objects.create(nombre_tema='Lectura',
                                            nombre_materia='Lengua',
                                            text_preg='harry potter es colorado?',
                                            reportada=False)
        question5 = Question.objects.create(nombre_tema='Lectura',
                                            nombre_materia='Lengua',
                                            text_preg='2 +2 ?',
                                            reportada=True)

    def test_question_up(self):
        """
        precondicion: simula ingresar pedido de redireccion.
        post :  compara si el resultado es la pagina con toda la estadisticas.
        """
        response = self.client.post(reverse('uploadquestion'), data={'namefile': '/questions/lxml.xml',
                                                                     'tipo': 'XML'})
        self.assertEqual(response.resolver_match.func, uploadquestion)

    def test_report_questions(self):
        response = self.client.post(reverse('reported'))
        self.assertEqual(response.resolver_match.func, reported)

    def test_agregar_pregunta(self):
        response = self.client.post(reverse('agregarPreg'), data={'materia': 'Matematica', 'tema': 'sumar',
                                                                  'titulo': '4 + 10 ?', 'opcion': 2,
                                                                  'opcion0': 24, 'opcion1': 14})
        self.assertEqual(response.resolver_match.func, agregarPreg)
