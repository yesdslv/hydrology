from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.encoding import force_text

from .views import home, search_hydropost_type, record

from .logged_in import LoggedInTestCase

from .models import Hydropost

class LoginPageTest(TestCase):
   
    def test_login_page_resolves_as_login_view(self):
        login_url = resolve('/login/')
        self.assertEqual(login_url.url_name, 'login')
    
    def test_not_logged_home_page_redirects_to_correct_url(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')

class HomePageTest(LoggedInTestCase):

    def test_root_url_resolves_as_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_view_uses_correct_template(self):
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hydrology/home.html')

    def test_static_javascript_included(self):
        response = self.client.post(reverse('home'))
        self.assertContains(response, 'hydrology/hydrology.js')

class HydropostCategorySearchPageTest(LoggedInTestCase):
    
    def test_record_url_resolves_as_data_view(self):
        found = resolve('/category/')
        self.assertEqual(found.func, search_hydropost_type)
    
    def test_view_return_correct_json_response(self):
        response = self.client.get(reverse('category'), { 'hydropost' : 'r. Esil - s. Derzhavinsk' })
        self.assertJSONEqual(force_text(response.content), { 'category': 'Речной пост 1 разряд' })
    
    def test_view_return_error_json_response_for_non_existing_hydropost(self):
        response = self.client.get(reverse('category'), { 'hydropost' : 'Non-existing hydropost' })
        self.assertJSONEqual(force_text(response.content), { 'error' : 'Нет такой станции' })

class RecordPageTest(LoggedInTestCase):

    def test_record_url_resolves_as_data_view(self):
        found = resolve('/record/')
        self.assertEqual(found.func, record)

    def test_request_get_correct_info(self):
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 1 разряд'},
        )
        self.assertEqual(response.status_code, 200)


