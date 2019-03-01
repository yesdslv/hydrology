from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.encoding import force_text

from .views import home, search_hydropost_category, record

import datetime

from .logged_in import LoggedInTestCase

from .models import Hydropost

from .forms import RHP1Form, RHP2Form, RHP3Form, LHP1Form, LHP2Form, SHP1Form, SHP2Form

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
        self.assertEqual(found.func, search_hydropost_category)
    
    def test_view_return_correct_json_response(self):
        response = self.client.get(reverse('category'), 
                { 'hydropost' : 'Р.Есиль – с. Державинск', },
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'category': 'Речной пост 1 разряд' })
    
    def test_view_return_error_json_response_for_non_existing_hydropost(self):
        response = self.client.get(reverse('category'), 
                { 'hydropost' : 'Non-existing hydropost', },
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'error' : 'Нет такой станции' })

class RecordPageTest(LoggedInTestCase):
    date = datetime.datetime.now()
    today_date = date.strftime('%Y-%m-%d')
    hour = date.strftime('%H')
    minute = date.strftime('%M')

    def test_record_url_resolves_as_data_view(self):
        found = resolve('/record/')
        self.assertEqual(found.func, record)

    def test_request_get_correct_info(self):
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 1 разряд', },
        )
        self.assertEqual(response.status_code, 200)

    def test_view_get_method_uses_correct_template(self):
        hydropost = Hydropost.objects.get(code = 11919)
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 1 разряд', },
        )
        self.assertTemplateUsed(response, 'hydrology/record.html')

    def test_record_page_uses_proper_form_for_RHP1(self):
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 1 разряд', },
        )
        self.assertIsInstance(response.context['form'], RHP1Form)

    def test_record_page_uses_proper_form_for_RHP2(self):
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 2 разряд', },
        )
        self.assertIsInstance(response.context['form'], RHP2Form)

    def test_record_page_uses_proper_form_for_RHP3(self):
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 3 разряд', },
        )
        self.assertIsInstance(response.context['form'], RHP3Form)

    def test_record_page_uses_proper_form_for_LHP1(self):
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Озерный пост 1 разряд', },
        )
        self.assertIsInstance(response.context['form'], LHP1Form)
    
    def test_record_page_uses_proper_form_for_LHP2(self):
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Озерный пост 2 разряд', },
        )
        self.assertIsInstance(response.context['form'], LHP2Form)
    
    def test_record_page_uses_proper_form_for_SHP1(self):
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Морской пост 1 разряд', },
        )
        self.assertIsInstance(response.context['form'], SHP1Form)

    def test_record_page_uses_proper_form_for_SHP2(self):
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Морской пост 2 разряд', },
        )
        self.assertIsInstance(response.context['form'], SHP2Form)

    def test_view_POST_min_data_and_return_correct_json_response(self):
        response = self.client.post(reverse('record'), 
            #Minimum data input are hydropost name, category, date, hour, minute, level
            #Category is required for creating required form in record view,
            #Level is required field in form
            data =  {
                'hydropost' : 'Р. Силеты – Новомарковка',
                'category' : 'Речной пост 1 разряд', 
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 10,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'done': 'done' })

    def test_view_POST_level_values_that_exceed_min_max_and_return_error_json_response(self):
        response = self.client.post(reverse('record'), 
            data =  {
                'hydropost' : 'Р. Силеты – Новомарковка',
                'category' : 'Речной пост 1 разряд', 
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 70000,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'error': 'Проверьте уровень воды' })

    def test_view_POST_water_temperature_values_that_exceed_min_max_and_return_error_json_response(self):
        response = self.client.post(reverse('record'), 
            data =  {
                'hydropost' : 'Р. Силеты – Новомарковка',
                'category' : 'Речной пост 1 разряд', 
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 6000,
                'water_temperature' : '80',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'error': 'Проверьте температуру воды' })

    def test_view_POST_air_temperature_values_that_exceed_min_max_and_return_error_json_response(self):
        response = self.client.post(reverse('record'), 
            data =  {
                'hydropost' : 'Р. Силеты – Новомарковка',
                'category' : 'Речной пост 1 разряд', 
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 6000,
                'air_temperature' : 500,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'error': 'Проверьте температуру воздуха' })

    def test_view_POST_ice_thickness_values_that_exceed_min_max_and_return_error_json_response(self):
        response = self.client.post(reverse('record'), 
            data =  {
                'hydropost' : 'Р. Силеты – Новомарковка',
                'category' : 'Речной пост 1 разряд', 
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 6000,
                'ice_thickness' : 200,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'error': 'Проверьте толщину льда' })

    def test_view_POST_precipitation_values_that_exceed_min_max_and_return_error_json_response(self):
        response = self.client.post(reverse('record'), 
            data =  {
                'hydropost' : 'Р. Силеты – Новомарковка',
                'category' : 'Речной пост 1 разряд', 
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 6000,
                'precipitation' : 2000,
                'precipitation_type' : 'жидкие',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'error': 'Проверьте количество осадков' })

    def test_view_POST_partial_precipitation_values_eturn_error_json_response(self):
        response = self.client.post(reverse('record'), 
            data =  {
                'hydropost' : 'Р. Силеты – Новомарковка',
                'category' : 'Речной пост 1 разряд', 
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 777,
                'precipitation' : 100,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'error': 'Заполните все поля осадков' })


    def test_view_POST_data_and_return_correct_json_response_for_RHP1(self):
        response = self.client.post(reverse('record'), 
            data =  { 
                'hydropost' : 'Р. Силеты – Новомарковка',
                'category' : 'Речной пост 1 разряд',
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 0,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'done': 'done' }) 

    def test_view_POST_data_and_return_correct_json_response_for_RHP2(self):
        response = self.client.post(reverse('record'), 
            data =  { 
                'hydropost' : 'р. Есиль - г.Астана',
                'category' : 'Речной пост 2 разряд',
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 0,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'done': 'done' }) 
    
    def test_view_POST_data_and_return_correct_json_response_for_RHP3(self):
        response = self.client.post(reverse('record'), 
            data =  { 
                'hydropost' : 'Р. Урал – г. Уральск',
                'category' : 'Речной пост 3 разряд',
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 0,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'done': 'done' }) 
    
    def test_view_POST_data_and_return_correct_json_response_for_LHP1(self):
        response = self.client.post(reverse('record'), 
            data =  { 
                'hydropost' : 'Вдхр. Буктырма– с. Аксуат',
                'category' : 'Озерный пост 1 разряд',
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 0,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'done': 'done' }) 
   
    def test_view_POST_data_and_return_correct_json_response_for_LHP2(self):
        response = self.client.post(reverse('record'), 
            data =  { 
                'hydropost' : 'Оз. Копа – г. Кокшетау',
                'category' : 'Озерный пост 2 разряд',
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 0,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'done': 'done' }) 
   
    def test_view_POST_data_and_return_correct_json_response_for_SHP1(self):
        response = self.client.post(reverse('record'), 
            data =  { 
                'hydropost' : 'Каспийское море – Форт Шевченко',
                'category' : 'Морской пост 1 разряд',
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 0,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'done': 'done' }) 
   
    def test_view_POST_data_and_return_correct_json_response_for_SHP2(self):
        response = self.client.post(reverse('record'), 
            data =  { 
                'hydropost' : 'Каспийское море – п.Каламкас',
                'category' : 'Морской пост 2 разряд',
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 0,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'done': 'done' }) 
