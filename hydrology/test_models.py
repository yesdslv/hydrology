from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

import datetime

from .models import Hydrologist, Hydropost, Observation, Measurement 
from .logged_in import LoggedInTestCase


class HydropostListModelTest(LoggedInTestCase):

    def test_get_hydrologist_see_his_region_hydroposts(self):
        user = User.objects.get(username = 'observer') 
        hydrologist = Hydrologist.objects.get(user = user)
        hydrologist_hydroposts = hydrologist.hydropost_set.all().values_list('name' , flat = True)
        his_hydroposts = ['Р. Силеты – Новомарковка', 
            'р. Есиль - г.Астана',
            'Р. Урал – г. Уральск',
            'Вдхр. Буктырма– с. Аксуат',
            'Оз. Копа – г. Кокшетау',
            'Каспийское море – Форт Шевченко',
            'Каспийское море – п.Каламкас',
        ]
        self.assertListEqual(list(hydrologist_hydroposts), list(his_hydroposts))


#We test model here, we assume we can input any observation
#for hydropost category. We restrict observation input by hydropost category
#in forms.py. Here we enter all observation data, no matter of hydropost category 
class ObservationModelTest(LoggedInTestCase):

    def test_hydrologist_enters_level(self):
        user = User.objects.get(username = 'observer')
        hydrologist = Hydrologist.objects.get(user = user)
        hydropost = Hydropost.objects.get(name = 'р. Есиль - г.Астана')
        #Time when hydrologist makes his observation
        observation_measurement_datetime = timezone.now() - datetime.timedelta(minutes=30)
        #Time when hydrologist enters data to database
        observation_input_datetime = timezone.now()

        #Observation contains hydropost id and hydrologist id
        observation = Observation.objects.get(Q(hydrologist = hydrologist) 
                & Q(hydropost = hydropost))
        hydropost_measurement = Measurement()
        hydropost_measurement.level = 800
        hydropost_measurement.observation = observation
        hydropost_measurement.observation_datetime = observation_measurement_datetime
        hydropost_measurement.entry_datetime = observation_input_datetime
        hydropost_measurement.save()

        retrieved_observation = Observation.objects.get(hydrologist = hydrologist, hydropost = hydropost)
        retrieved_measurement = Measurement.objects.get(Q(observation = retrieved_observation) 
                & Q(observation_datetime = observation_measurement_datetime))
        self.assertEqual(hydropost_measurement.level, retrieved_measurement.level)
        self.assertEqual(hydropost_measurement.observation_datetime, retrieved_measurement.observation_datetime)
        self.assertEqual(hydropost_measurement.entry_datetime, retrieved_measurement.entry_datetime)
