from django.test import TestCase
from django.core.urlresolvers import reverse
from allauth.account.forms import BaseSignupForm
from django.test.client import Client
from allauth.utils import get_user_model


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

	def test_signup_username_already_exist(self):
		user = get_user_model().objects.create(
			username='pedro',
			is_active=True)
		response = self.client.post(
				reverse('account_signup'),
				data={
					'username': 'pedro',
					'email': 'pedro@test.com',
					'password1': 'pepito12',
					'password2': 'pepito12'})
		self.assertFormError(
			response,
			'form',
			'username',
			'A user with that username already exists.'
		)