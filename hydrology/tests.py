from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView

from .views import home

class LoginPageTest(TestCase):
   
    def test_login_page_resolves_as_login_view(self):
        login_url = resolve('/login/')
        self.assertEqual(login_url.url_name, 'login')

