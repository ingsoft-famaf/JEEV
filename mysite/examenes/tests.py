from django.test import TestCase
from django.core.urlresolvers import reverse
from allauth.account.forms import BaseSignupForm
from django.test.client import Client
from allauth.utils import get_user_model
from examenes.models import Exam
from questions.models import Question, Answer
from examenes.views import *


class ExamTest(TestCase):

    def setUp(self):
        question1 = Question.objects.create(nombre_tema='sumar', nombre_materia='Matematicas',
                                            text_preg='2 + 2 ?', reportada=False)
        Answer.objects.create(respuesta=question1, text_resp='4', es_correcta=True)
        Answer.objects.create(respuesta=question1, text_resp="5", es_correcta=False)
        Answer.objects.create(respuesta=question1, text_resp="7", es_correcta=False)
        Answer.objects.create(respuesta=question1, text_resp="9", es_correcta=False)
        question2 = Question.objects.create(nombre_tema='sumar', nombre_materia='Matematicas',
                                            text_preg='5 x 5 ?', reportada=False)
        question3 = Question.objects.create(nombre_tema='sumar', nombre_materia='Matematicas',
                                            text_preg='5 + 2 ?', reportada=False)
        question4 = Question.objects.create(nombre_tema='sumar', nombre_materia='Matematicas',
                                            text_preg='24 x 2 ?', reportada=False)
        question5 = Question.objects.create(nombre_tema='Lectura', nombre_materia='Lengua',
                                            text_preg='frodo amigo de sam?', reportada=False)
        question6 = Question.objects.create(nombre_tema='Lectura', nombre_materia='Lengua',
                                            text_preg='harry potter es colorado?', reportada=False)
        question7 = Question.objects.create(nombre_tema='Lectura', nombre_materia='Lengua',
                                            text_preg='2 +2 ?', reportada=False)
        examen1 = Exam.objects.create(nombre_materia='Matematicas', cantidad_preg=3, tiempo_preg=15)
        examen2 = Exam.objects.create(nombre_materia='Lengua', cantidad_preg=3, tiempo_preg=9)

    def test_set_up_exam(self):
        """crea y simila subir datos de un examen, para comparar con la funcion examenencurso_view.
        precondicion: simulo subir datos del examen a testear
        postcondicion: devuelve un error o si el test haya pasado bien, sigue.
                      compara la funcion examenencurso pasando como datos lo creado.
        """
        response = self.client.post(reverse('examenencurso'),
                                    data={
                                        'materias': 'Legua',
                                        'temas': 'Lectura',
                                        'cantidad': 1,
                                        'tiempo': 10})
        self.assertEqual(response.resolver_match.func, examenencurso_view)

    def test_reportar(self):
        """
        crea un examen con el atributo nombre de materia, pregunta y simulo enviar datos,
        Compara que si las preguntas tengan respuestas.
        precondicion: simulo subir nombre del examen, una preg a testear
        postcondicion: devuelve un error o si el test haya pasado bien, sigue.
        compara la funcion resppreg, donde muestra una preg
        con sus resp.
        """
        examen = Exam.objects.get(nombre_materia='Matematicas')
        pregunta = Question.objects.get(text_preg='2 + 2 ?')
        response = self.client.get(reverse('reportar', args=[examen.id, pregunta.id]))
        self.assertEqual(response.resolver_match.func, reportar)
