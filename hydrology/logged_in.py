from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import resolve, reverse
from django.core.management import call_command
from django.utils import timezone
from django.db.models import Q

import datetime

from .models import Hydrologist, Hydropost, Observation, Measurement 

#Create three users
#First is observer, assign to him observed hydroposts
#Second engineer
#Third hydrologist, in hydrologist model default occupation value observer  
class LoggedInTestCase(TestCase):
    fixtures = ['hydrology/fixtures/fixtures.json']
    
    def setUp(self):
        #Create user
        new_user = User.objects.create_user(username='observer', password='password', 
                first_name = 'Наблюдатель', last_name = 'Наблюдаев')
        #Assign user to observers
        new_hydrologist = Hydrologist.objects.create(
                user = new_user,
                occupation = Hydrologist.OBSERVER,        
        )  
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
        ##Observer will enter data for these hydroposts
        first_hydropost_observation = Observation.objects.create(hydropost = firstHydropost,
                            hydrologist = new_hydrologist)
        second_hydropost_observation = Observation.objects.create(hydropost = secondHydropost,
                            hydrologist = new_hydrologist)
        third_hydropost_observation = Observation.objects.create(hydropost = thirdHydropost,
                            hydrologist = new_hydrologist)
        fourth_hydropost_observation = Observation.objects.create(hydropost = fourthHydropost,
                            hydrologist = new_hydrologist)
        fifth_hydropost_observation = Observation.objects.create(hydropost = fifthHydropost,
                            hydrologist = new_hydrologist)
        sixth_hydropost_observation = Observation.objects.create(hydropost = sixthHydropost,
                            hydrologist = new_hydrologist)
        seventh_hydropost_observation = Observation.objects.create(hydropost = seventhHydropost,
                            hydrologist = new_hydrologist)

        observations = Observation.objects.filter(hydrologist = new_hydrologist)  
        #Create new user
        new_user = User.objects.create_user(username='engineer', password='password')
        #Assign user to engineers
        new_hydrologist = Hydrologist.objects.create(
                user = new_user,
                occupation = Hydrologist.ENGINEER,
        )
        #Create new user
        new_user = User.objects.create_user(username='hydrologist', password='password')
        new_hydrologist = Hydrologist.objects.create(user = new_user)
        #Start point for datetime
        init_datetime = datetime.datetime.strptime('2019-03-01 10:00:00', '%Y-%m-%d %H:%M:%S')
        #Create 5 days Level observation for Р. Силеты – Новомарковка(11242)
        for day in range(5):
            #Input some observation data
            #Time when observer makes his observation
            observation_measurement_datetime = init_datetime - datetime.timedelta(days = day, minutes=30)
            #Remove seconds and microseconds
            observation_measurement_datetime = observation_measurement_datetime.replace( second = 0, microsecond = 0)
            #Time when observer enters data
            observation_entry_datetime = init_datetime - datetime.timedelta(days = day)
            #Remove seconds
            observation_entry_datetime = observation_entry_datetime.replace(second = 0)
            Measurement.objects.create(
                level = 100,
                air_temperature = 10,
                observation_datetime = observation_measurement_datetime,
                entry_datetime = observation_entry_datetime,
                observation = first_hydropost_observation,
            )
