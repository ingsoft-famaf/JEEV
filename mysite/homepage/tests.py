from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from homepage.views import *


class HomeTests(TestCase):

    def test_redirijido_al_home(self):
        response = self.client.get(reverse('homepage'))
        self.assertEquals(response.resolver_match.func, homepage)


class TemaMethodTests(TestCase):

    def test_redirijido_al_home(self):
        pass
