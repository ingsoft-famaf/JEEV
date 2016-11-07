from django.test import TestCase
from django.test.client import Client

class QuestionTest(TestCase):
        
    def test_redirect_question_reported(self):
        response = self.client.get('/superuser/')
        self.assertRedirects(response, '/questions/reported/')
