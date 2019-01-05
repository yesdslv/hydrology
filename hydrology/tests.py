from django.test import TestCase
from django.urls import resolve


class HomePageTest(TestCase):
    
    def test_root_page_resolves_as_home_url_view(self):
