from django.test import TestCase
from django.test import Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.utils.encoding import force_text

from .views import home, record 

from .models import Hydropost, Hydrologist, Region, Observation

from .forms import GP1Form, OGP2Form

class LoginPageTest(TestCase):
   
    def test_login_page_resolves_as_login_view(self):
        login_url = resolve('/login/')
        self.assertEqual(login_url.url_name, 'login')
    
    def test_not_logged_home_page_redirects_to_correct_url(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')

class LoggedInTestCase(TestCase):
    fixtures = ['hydrology/fixtures/fixtures.json']
    
    def setUp(self):
        new_user = User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')
        new_hydrologist = Hydrologist.objects.create(user = new_user)  
        #Р. Силеты – Новомарковка
        #nameEn r. Silety - Novomarkovka
        #ГП-1
        firstHydropost = Hydropost.objects.get(code = 11242)
        #Р.Есиль – с. Державинск
        #nameEn r. Esil - s. Derzhavinsk
        #ГП-1
        secondHydropost = Hydropost.objects.get(code = 11402)
        #Оз. Копа – г. Кокшетау
        #Oz. Kopa - g. Kokshetau
        #ОГП-2
        thirdHydropost = Hydropost.objects.get(code = 11919)        
        Observation.objects.create(hydropost = firstHydropost,
                hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = secondHydropost,
                hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = thirdHydropost,
                hydrologist = new_hydrologist)
        

class HomePageTest(LoggedInTestCase):

    def test_root_url_resolves_as_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_view_uses_correct_template(self):
        response = self.client.post(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'hydrology/home.html')

    def test_view_return_correct_json_response(self):
        response = self.client.get(reverse('home'), { 'hydropost' : 'r. Esil - s. Derzhavinsk' })
        self.assertJSONEqual(force_text(response.content), { 'success': 'Речной пост 1 разряд' })
    
    def test_view_return_error_json_response_for_non_existing_hydropost(self):
        response = self.client.get(reverse('home'), { 'hydropost' : 'Non-existing hydropost' })
        self.assertJSONEqual(force_text(response.content), { 'error' : 'Нет такой станции' })

class HydropostListModelTest(LoggedInTestCase):

    def test_get_hydrologist_see_his_region_hydroposts(self):
        user = User.objects.get(username = 'username') 
        hydrologist = Hydrologist.objects.get(user = user)
        hydrologist_hydroposts = hydrologist.hydropost_set.all().values_list('name' , flat = True)
        his_hydroposts = ['Р. Силеты – Новомарковка', 
                'Р.Есиль – с. Державинск', 'Оз. Копа – г. Кокшетау']        
        self.assertListEqual(list(hydrologist_hydroposts), list(his_hydroposts))

class RecordPageTest(LoggedInTestCase):

    def test_record_url_resolves_as_data_view(self):
        found = resolve('/record/')
        self.assertEqual(found.func, record)

    def test_view_uses_correct_template(self):
        hydropost = Hydropost.objects.get(code = 11242)
        response = self.client.post(
            '/record/',
            data = { 'hydropost' : hydropost.nameEn ,}
        )
        self.assertTemplateUsed(response, 'hydrology/record.html')

    def test_request_post_correct_info(self):
        hydropost = Hydropost.objects.get(code = 11402)
        response = self.client.post(
            '/record/',
            data = { 'hydropost' : hydropost.nameEn ,}
        )
        self.assertEquals(response.status_code, 200)

    def test_record_page_uses_proper_form_for_GP1(self):
        hydropost = Hydropost.objects.get(code = 11402)
        response = self.client.post(
            '/record/',
            data = { 'hydropost' : hydropost.nameEn ,}
        )
        self.assertIsInstance(response.context['form'], GP1Form)

    #def test_record_page_uses_proper_form_for_OGP2(self):
    #    hydropost = Hydropost.objects.get(code = 11919)
    #    response = self.client.post(
    #        '/record/',
    #        data = { 'hydropost' : hydropost.nameEn ,}
    #    )
    #    self.assertIsInstance(response.context['form'], OGP2Form)

class ObservationFormTest(TestCase):

    ##Form for Речной пост 1 разряд
    def test_GP1_form_contains_all_observation_for_his_types(self):
       form = GP1Form()
       self.assertIn('name="level"', form.as_p())
       self.assertIn('name="discharge"', form.as_p())
       self.assertIn('name="air_temperature"', form.as_p())
       self.assertIn('name="water_temperature"', form.as_p())

    def test_OGP2_form_contains_all_observation_for_his_type(self):
       form = OGP2Form()
       self.assertIn('name="air_temperature"', form.as_p())
       self.assertIn('name="water_temperature"', form.as_p())
       self.assertIn('name="ripple"', form.as_p())
       self.assertIn('name="level"', form.as_p())

#class HydropostTypePageTest(TestCase):


