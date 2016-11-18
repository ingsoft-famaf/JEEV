from django.test import TestCase
from django.core.urlresolvers import reverse
from allauth.account.forms import BaseSignupForm
from django.test.client import Client
from allauth.utils import get_user_model
from django.contrib.auth.models import User


class AccountTest(TestCase):

    def test_signup_password_twice_form_error(self):
        response = self.client.post(reverse('account_signup'),
                                    data={'username': 'pedro',
                                          'email': 'pedro@test.com',
                                          'password1': 'pepito12',
                                          'password2': 'pepoti12'})
        self.assertContains(response, 'You must type the same password each time.')

    def test_signup_password_too_short(self):
        response = self.client.post(reverse('account_signup'),
                                    data={'seranme': 'pedro',
                                          'email': 'pedro@test.com',
                                          'password1': 'pepi',
                                          'password2': 'pepi'})
        self.assertContains(response, 'This password is too short. It must contain at least 8 characters.')

    def test_signup_password_similar_username(self):
        response = self.client.post(reverse('account_signup'),
                                    data={'username': 'pepito',
                                          'email': 'pepito@test.com',
                                          'password1': 'pepito12',
                                          'password2': 'pepito12'})
        self.assertContains(response, 'The password is too similar to the username.')

    def test_signup_username_already_exist(self):
        user = get_user_model().objects.create(
            username='pedro',
            is_active=True)
        response = self.client.post(reverse('account_signup'),
                                    data={'username': 'pedro',
                                          'email': 'pedro@test.com',
                                          'password1': 'pepito12',
                                          'password2': 'pepito12'})
        self.assertContains(response, 'A user with that username already exists.')

    def test_signup_email_already_exist(self):
        user = get_user_model().objects.create(username='juan',
                                               email='pedro@test.com',
                                               is_active=True)
        response = self.client.post(reverse('account_signup'),
                                    data={'username': 'pedro',
                                          'email': 'pedro@test.com',
                                          'password1': 'pepito12',
                                          'password2': 'pepito12'})
        self.assertContains(response, 'A user is already registered with this e-mail address.')

    def _create_new_user(self):
        password = 'asd123'
        my_admin = User.objects.create_superuser('myuser', 'myuser@test.com', password)
        c = Client()
        c.login(username=my_admin.username, password=password)
        return c

    def test_redirect_when_authenticated(self):
        c = self._create_new_user()
        resp = c.get(reverse('account_login'))
        self.assertRedirects(resp, '/accounts/profile/', fetch_redirect_response=False)
