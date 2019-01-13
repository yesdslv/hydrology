from django.test import TestCase
from django.test import Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.contrib.auth.models import User

from .views import home

from .models import Hydropost, Hydrologist, Region, Observation

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
        firstHydropost = Hydropost.objects.get(code = 11242)
        #Р.Есиль – с. Державинск
        secondHydropost = Hydropost.objects.get(code = 11402)
        Observation.objects.create(hydropost = firstHydropost,
                hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = secondHydropost,
                hydrologist = new_hydrologist)


class HomePageTest(LoggedInTestCase):

    def test_root_url_resolves_as_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'hydrology/home.html')



class HydropostListModelTest(LoggedInTestCase):

    def test_get_hydrologist_see_his_region_hydroposts(self):
        user = User.objects.get(username = 'username') 
        hydrologist = Hydrologist.objects.get(user = user)
        hydrologist_hydroposts = hydrologist.hydropost_set.all().values_list('name' , flat = True)
        his_hydroposts = ['Р. Силеты – Новомарковка', 'Р.Есиль – с. Державинск']        
        self.assertListEqual(list(hydrologist_hydroposts), list(his_hydroposts))
