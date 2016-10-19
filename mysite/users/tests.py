from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from allauth.utils import get_user_model
from django.contrib.auth.models import User


class LoginTest(TestCase):

	def _create_new_user(self):
		password ='asd123'
		my_admin = User.objects.create_superuser('myuser','myuser@test.com', password)
		c = Client()
		c.login(username=my_admin.username, password=password)
		return c

	def test_redirect_when_authenticated(self):
		c = self._create_new_user()
		resp = c.get(reverse('account_login'))
		self.assertRedirects(resp, '/accounts/profile/', fetch_redirect_response=False)