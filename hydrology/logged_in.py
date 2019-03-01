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
        ##Р. Силеты – Новомарковка
        ##r. Silety - Novomarkovka
        ##Тип ГП-1
        firstHydropost = Hydropost.objects.get(code = 11242)
        ##р. Есиль - г.Астана
        ##r. Esil - g. Astana
        ##Тип ГП-2
        secondHydropost = Hydropost.objects.get(code = 11398)
        ##Р. Урал – г. Уральск
        ##R. Ural – g. Uralsk
        ##Тип ГП-3
        thirdHydropost = Hydropost.objects.get(code = 19071)
        ##Вдхр. Буктырма– с. Аксуат
        ##vdhr. Buktyrma - s. Aksuat
        ##Тип ОГП-1
        fourthHydropost = Hydropost.objects.get(code = 2300738)
        ##Оз. Копа – г. Кокшетау
        ##Oz. Kopa - g. Kokshetau
        ##Тип ОГП-2
        fifthHydropost = Hydropost.objects.get(code = 11919)
        ##Каспийское море – Форт Шевченко        
        ##Kaspiyskoye more – Fort Shevchenko
        ##Тип МГП-1
        sixthHydropost = Hydropost.objects.get(code = 97060)
        ##Каспийское море – п.Каламкас
        ##Kaspiyskoye more – p.Kalamkas
        ##Тип МГП-2
        seventhHydropost = Hydropost.objects.get(code = 97057)
        ##Didar will enter data for these hydroposts
        Observation.objects.create(hydropost = firstHydropost,
                            hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = secondHydropost,
                            hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = thirdHydropost,
                            hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = fourthHydropost,
                            hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = fifthHydropost,
                            hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = sixthHydropost,
                            hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = seventhHydropost,
                            hydrologist = new_hydrologist)
