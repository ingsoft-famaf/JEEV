from django.test import TestCase
from django.core.urlresolvers import reverse
from allauth.account.forms import BaseSignupForm
from django.test.client import Client
from allauth.utils import get_user_model
from examenes.models import Exam
from questions.models import Question, Answer
from examenes.views import *
from questions.views import *



class QuestionTest(TestCase):


    def setUp(self):
        examen1 = Exam.objects.create(nombre_materia='Matematicas',
                                      nombre_tema='sumar',
                                      cantidad_preg=3,
                                      tiempo_preg=15)
        examen2 = Exam.objects.create(nombre_materia='Lengua',
                                      nombre_tema='Lectura',
                                      cantidad_preg=3,
                                      tiempo_preg=9)
        
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
                                            reportada=False)

    def test_question_up(self):
        #response = self.client.post(),
        response = self.client.post(reverse('uploadquestion'), data={ 'namefile':'/questions/lxml.xml'})
        self.assertEqual(response.resolver_match.func, uploadquestion)

    def test_report_questions(self):
        q = Question.objects.post(reportada=False)
        response = self.client.post(reverse('question'), q)
        self.assertEqual(response.resolver_match.func, reported)
