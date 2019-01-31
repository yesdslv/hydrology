from django.test import TestCase
from django.contrib.auth.models import User

from .models import Hydrologist

from .logged_in import LoggedInTestCase

class HydropostListModelTest(LoggedInTestCase):

    def test_get_hydrologist_see_his_region_hydroposts(self):
        user = User.objects.get(username = 'username') 
        hydrologist = Hydrologist.objects.get(user = user)
        hydrologist_hydroposts = hydrologist.hydropost_set.all().values_list('name' , flat = True)
        his_hydroposts = ['Р. Силеты – Новомарковка', 
                'Р.Есиль – с. Державинск', 'Оз. Копа – г. Кокшетау']        
        self.assertListEqual(list(hydrologist_hydroposts), list(his_hydroposts))


