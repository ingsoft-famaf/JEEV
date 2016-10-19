from django.test import TestCase
from django.core.urlresolvers import reverse
from allauth.account.forms import BaseSignupForm
from django.test.client import Client


class SignupTest(TestCase):

	def test_signup_password_twice_form_error(self):
		response = self.client.post(
				reverse('account_signup'),
				data={
					'username': 'pedro',
					'email': 'pedro@test.com',
					'password1': 'pepito12',
					'password2': 'pepoti12'})
		self.assertFormError(
			response,
			'form',
			'password2',
			'You must type the same password each time.'
		)