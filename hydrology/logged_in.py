from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import resolve, reverse

from .models import Hydrologist, Hydropost, Observation

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


