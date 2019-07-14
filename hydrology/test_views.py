from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.encoding import force_text
from django.utils import timezone

from .views import observation, search_hydropost_category, record, home, data

from datetime import datetime, timedelta

from .logged_in import LoggedInTestCase 

from .models import Hydropost

from .forms import RHP1Form, RHP2Form, RHP3Form, LHP1Form, LHP2Form, SHP1Form, SHP2Form

import json

class LoginViewTest(TestCase):
   
    def test_login_page_resolves_as_login_view(self):
        login_url = resolve('/login/')
        self.assertEqual(login_url.url_name, 'login')
    
    def test_not_logged_home_page_redirects_to_correct_url(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')

class ObservationViewTest(LoggedInTestCase):

    def test_observation_url_resolves_as_observation_view(self):
        self.client.login(username = 'observer', password = 'password') 
        found = resolve('/observation/')
        self.assertEqual(found.func, observation)

    def test_view_uses_correct_template(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.post(reverse('observation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hydrology/observation.html')

    def test_static_javascript_included(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.post(reverse('observation'))
        self.assertContains(response, 'hydrology/hydrology.js')

class HydropostCategorySearchiViewTest(LoggedInTestCase):
    
    def test_record_url_resolves_as_data_view(self):
        self.client.login(username = 'observer', password = 'password') 
        found = resolve('/category/')
        self.assertEqual(found.func, search_hydropost_category)
    
    def test_view_return_correct_json_response(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.get(reverse('category'), 
                { 'hydropost' : 'Р.Есиль – с. Державинск', },
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'category': 'Речной пост 1 разряд' })
    
    def test_view_return_error_json_response_for_non_existing_hydropost(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.get(reverse('category'), 
                { 'hydropost' : 'Non-existing hydropost', },
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'error' : 'Нет такой станции' })

class RecordViewTest(LoggedInTestCase):

    def test_record_url_resolves_as_record_view(self):
        self.client.login(username = 'observer', password = 'password') 
        found = resolve('/record/')
        self.assertEqual(found.func, record)

    def test_request_get_correct_info(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 1 разряд', },
        )
        self.assertEqual(response.status_code, 200)

    def test_view_get_method_uses_correct_template(self):
        self.client.login(username = 'observer', password = 'password') 
        hydropost = Hydropost.objects.get(code = 11919)
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 1 разряд', },
        )
        self.assertTemplateUsed(response, 'hydrology/record.html')

    def test_record_page_uses_proper_form_for_RHP1(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 1 разряд', },
        )
        self.assertIsInstance(response.context['form'], RHP1Form)

    def test_record_page_uses_proper_form_for_RHP2(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 2 разряд', },
        )
        self.assertIsInstance(response.context['form'], RHP2Form)

    def test_record_page_uses_proper_form_for_RHP3(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Речной пост 3 разряд', },
        )
        self.assertIsInstance(response.context['form'], RHP3Form)

    def test_record_page_uses_proper_form_for_LHP1(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Озерный пост 1 разряд', },
        )
        self.assertIsInstance(response.context['form'], LHP1Form)
    
    def test_record_page_uses_proper_form_for_LHP2(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Озерный пост 2 разряд', },
        )
        self.assertIsInstance(response.context['form'], LHP2Form)
    
    def test_record_page_uses_proper_form_for_SHP1(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Морской пост 1 разряд', },
        )
        self.assertIsInstance(response.context['form'], SHP1Form)

    def test_record_page_uses_proper_form_for_SHP2(self):
        self.client.login(username = 'observer', password = 'password') 
        response = self.client.get(
            '/record/',
            data = { 'category' : 'Морской пост 2 разряд', },
        )
        self.assertIsInstance(response.context['form'], SHP2Form)

    def test_view_POST_min_data_and_return_correct_json_response(self):
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 1)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 2)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 3)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 4)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 5)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 6)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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

    def test_view_POST_partial_precipitation_values_return_error_json_response(self):
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 7)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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

    def test_view_POST_multiple_water_object_condition_and_return_correct_json_response(self):
        self.client.login(username = 'observer', password = 'password')
        date = datetime.now() - timedelta(hours = 8)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
        response = self.client.post(reverse('record'), 
            data =  { 
                'hydropost' : 'Р. Силеты – Новомарковка',
                'category' : 'Речной пост 1 разряд',
                'date' : today_date,
                'hour' : hour,
                'minute' : minute,
                'level' : 0,
                'water_object_condition' : ['Сало', 'Снежура',],
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertJSONEqual(force_text(response.content), { 'done': 'done' }) 



    def test_view_POST_data_and_return_correct_json_response_for_RHP1(self):
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 9)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 10)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 11)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now() - timedelta(hours = 12)
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now()
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now()
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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
        self.client.login(username = 'observer', password = 'password') 
        date = datetime.now()
        today_date = date.strftime('%Y-%m-%d')
        hour = date.strftime('%H')
        minute = date.strftime('%M')
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

class DataViewTest(LoggedInTestCase):
    
    def test_data_url_resolves_as_data_view(self):
        self.client.login(username='engineer', password='password1')
        found = resolve('/data/')
        self.assertEqual(found.func, data)
    
    def test_static_javascript_included(self):
        self.client.login(username='engineer', password='password')
        response = self.client.get(reverse('data'))
        self.assertContains(response, 'hydrology/data.js')
    
    def test_POST_start_datetime_and_end_datetime_and_return_correct_json_response(self):
        #Observation is recorded in logged_in
        #Start_datetime should be less than observation_measurement_datetime - 5 days in logged_in
        #End_datetime should be greater than observation_measurement_datetime in logged_in
        self.client.login(username='engineer', password='password')
        #Datatable POST some additional data, table view use:
        #Start, length, order[0]column, order[0][dir], search[value], draw
        response = self.client.post(reverse('data'),
            data = { 
                'start_datetime' : '2019-01-01 00:00',
                'end_datetime' : '2019-03-20 00:00',
                'start' : 0,
                'length' : 5,
                'order[0][column]' : 2,
                'order[0][dir]' : 'asc',
                'search[value]' : '',
                'draw' : 0
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
         
        observation_datetimes = []
        entry_datetimes = []
        init_datetime = datetime.strptime('2019-03-01 10:00:00', '%Y-%m-%d %H:%M:%S')
        for day in range(5):
            #Time when observer makes his observation
            observation_measurement_datetime = init_datetime - timedelta(days = day, minutes=30)
            #Remove seconds and microseconds
            observation_measurement_datetime = observation_measurement_datetime.replace( second = 0, microsecond = 0)
            #Time when observer enters data
            observation_entry_datetime = init_datetime - timedelta(days = day)
            #Remove seconds
            observation_entry_datetime = observation_entry_datetime.replace(second = 0)
            observation_datetimes.append(observation_measurement_datetime)
            entry_datetimes.append(observation_entry_datetime)
 
        expected_result = {
            'recordsTotal' : 5,
            'recordsFiltered' : 5,
            'draw' : 0,
            'data' : [
                {
                    'hydropost_name' : 'Р. Силеты – Новомарковка',
                    'hydropost_code' : 11242,
                    'region' : 'Акмолинская область',
                    'observer' : 'Наблюдатель Наблюдаев',
                    'observation_datetime' : observation_datetimes[0].strftime('%Y-%m-%dT%H:%M:%S'),
                    'entry_datetime' : entry_datetimes[0].strftime('%Y-%m-%dT%H:%M:%S'),
                    'level' : 100,
                    'water_temperature' : None,
                    'air_temperature' : 10,
                    'precipitation' : None,
                    'precipitation_type' : None,
                    'wind_direction' : None,
                    'wind_power' : None,
                },
                {
                    'hydropost_name' : 'Р. Силеты – Новомарковка',
                    'hydropost_code' : 11242,
                    'region' : 'Акмолинская область',
                    'observer' : 'Наблюдатель Наблюдаев',
                    'observation_datetime' : observation_datetimes[1].strftime('%Y-%m-%dT%H:%M:%S'),
                    'entry_datetime' : entry_datetimes[1].strftime('%Y-%m-%dT%H:%M:%S'),
                    'level' : 100,
                    'water_temperature' : None,
                    'air_temperature' : 10,
                    'precipitation' : None,
                    'precipitation_type' : None,
                    'wind_direction' : None,
                    'wind_power' : None,
                },
                {
                    'hydropost_name' : 'Р. Силеты – Новомарковка',
                    'hydropost_code' : 11242,
                    'region' : 'Акмолинская область',
                    'observer' : 'Наблюдатель Наблюдаев',
                    'observation_datetime' : observation_datetimes[2].strftime('%Y-%m-%dT%H:%M:%S'),
                    'entry_datetime' : entry_datetimes[2].strftime('%Y-%m-%dT%H:%M:%S'),
                    'level' : 100,
                    'water_temperature' : None,
                    'air_temperature' : 10,
                    'precipitation' : None,
                    'precipitation_type' : None,
                    'wind_direction' : None,
                    'wind_power' : None,
                },
                {
                    'hydropost_name' : 'Р. Силеты – Новомарковка',
                    'hydropost_code' : 11242,
                    'region' : 'Акмолинская область',
                    'observer' : 'Наблюдатель Наблюдаев',
                    'observation_datetime' : observation_datetimes[3].strftime('%Y-%m-%dT%H:%M:%S'),
                    'entry_datetime' : entry_datetimes[3].strftime('%Y-%m-%dT%H:%M:%S'),
                    'level' : 100,
                    'water_temperature' : None,
                    'air_temperature' : 10,
                    'precipitation' : None,
                    'precipitation_type' : None,
                    'wind_direction' : None,
                    'wind_power' : None,
                },
                {
                    'hydropost_name' : 'Р. Силеты – Новомарковка',
                    'hydropost_code' : 11242,
                    'region' : 'Акмолинская область',
                    'observer' : 'Наблюдатель Наблюдаев',
                    'observation_datetime' : observation_datetimes[4].strftime('%Y-%m-%dT%H:%M:%S'),
                    'entry_datetime' : entry_datetimes[4].strftime('%Y-%m-%dT%H:%M:%S'),
                    'level' : 100,
                    'water_temperature' : None,
                    'air_temperature' : 10,
                    'precipitation' : None,
                    'precipitation_type' : None,
                    'wind_direction' : None,
                    'wind_power' : None,
                }
            ]
        }
        print(type(expected_result))
        print(expected_result['data'])
        expected_result = json.dumps(expected_result)
        json_expected_result = json.loads(expected_result)
        self.maxDiff = None
        self.assertJSONEqual(force_text(response.content), json_expected_result)
