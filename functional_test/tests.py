from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import unittest

import time

from hydrology.models import Hydropost, Hydrologist, Observation

class VisitorLoginTest(StaticLiveServerTestCase):
    fixtures = ['hydrology/fixtures/fixtures.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        ##Create user Didar and make him hydrologist
        new_user = User.objects.create_user(username = 'Didar', password = 'password')
        new_hydrologist = Hydrologist.objects.create(user = new_user)  
        ##Р. Силеты – Новомарковка
        ##Тип ГП-1
        firstHydropost = Hydropost.objects.get(code = 11242)
        ##р. Есиль - г.Астана
        ##Тип ГП-2
        secondHydropost = Hydropost.objects.get(code = 11398)
        ##Р. Урал – г. Уральск
        ##Тип ГП-3
        thirdHydropost = Hydropost.objects.get(code = 19071)
        ##Вдхр. Буктырма– с. Аксуат
        ##Тип ОГП-1
        fourthHydropost = Hydropost.objects.get(code = 2300738)
        ##Оз. Копа – г. Кокшетау
        ##Тип ОГП-2
        fifthHydropost = Hydropost.objects.get(code = 11919)
        ##Каспийское море – Форт Шевченко        
        ##Тип МГП-1
        sixthHydropost = Hydropost.objects.get(code = 97060)
        ##Каспийское море – п.Каламкас
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

    def tearDown(self):
        self.browser.quit()

    def checkForRowInListTable(self, rowText):
        table = self.browser.find_element_by_name('hydropost')
        rows = table.find_elements_by_tag_name('option')
        self.assertIn(rowText, [row.text for row in rows])

    def selectHydropost(self, hydropost_name, hydropost_category):
        #Hydrologist select one hydropost
        select = Select(self.browser.find_element_by_name('hydropost'))
        #select.select_by_visible_text(hydropost_name)
        select.select_by_visible_text(hydropost_name)
        #Hydrologist should see hydropost category in header h3
        ##That one is for testing get request 
        ##We get hydropost category
        time.sleep(1)

    def submitObservationData(self, hydropost_name, hydropost_category):
        self.selectHydropost(hydropost_name, hydropost_category)
        observation_button = self.browser.find_element_by_id('modalTrigger')
        observation_button.click()
        #He should see modal with input
        #Modal hydropost headers should be equal to hydropost name
        modal_hydropost_title = self.browser.find_element_by_id('hydropost')
        self.assertEqual(modal_hydropost_title.text, hydropost_name)
        #Modal category header should be equal to hydropost category
        modal_category_title = self.browser.find_element_by_id('category')
        self.assertEqual(modal_category_title.text, hydropost_category)
        #He should see input form for Речной пост 1 разряд category
        if hydropost_category == 'Речной пост 1 разряд':
            level_input = self.browser.find_element_by_name('level')
            water_temperature_input = self.browser.find_element_by_name('water_temperature')
            air_temperature_input = self.browser.find_element_by_name('air_temperature')
            ice_thickness_input = self.browser.find_element_by_name('ice_thickness')
            level_input.send_keys('12')
            time.sleep(2)
        #He should see input form for Речной пост 2 разряд category
        elif hydropost_category == 'Речной пост 2 разряд': 
            level_input = self.browser.find_element_by_name('level')
            water_temperature_input = self.browser.find_element_by_name('water_temperature')
            air_temperature_input = self.browser.find_element_by_name('air_temperature') 
            ice_thickness_input = self.browser.find_element_by_name('ice_thickness')
            level_input.send_keys('12')
            time.sleep(2)
        #He should see input form for Речной пост 3 разряд category
        elif hydropost_category == 'Речной пост 3 разряд': 
            level_input = self.browser.find_element_by_name('level')
            water_temperature_input = self.browser.find_element_by_name('water_temperature')
            air_temperature_input = self.browser.find_element_by_name('air_temperature') 
            ice_thickness_input = self.browser.find_element_by_name('ice_thickness')
            level_input.send_keys('12')
            time.sleep(2)
        #He should see input form for Озерный пост 1 разряд category
        elif hydropost_category == 'Озерный пост 1 разряд':
            level_input = self.browser.find_element_by_name('level')
            ripple_input = self.browser.find_element_by_name('ripple')
            water_temperature_input = self.browser.find_element_by_name('water_temperature')
            air_temperature_input = self.browser.find_element_by_name('air_temperature') 
            ice_thickness_input = self.browser.find_element_by_name('ice_thickness')
            level_input.send_keys('12')
            time.sleep(2)
        #He should see input form for Озерный пост 2 разряд category
        elif hydropost_category == 'Озерный пост 2 разряд': 
            level_input = self.browser.find_element_by_name('level')
            ripple_input = self.browser.find_element_by_name('ripple')
            water_temperature_input = self.browser.find_element_by_name('water_temperature')
            air_temperature_input = self.browser.find_element_by_name('air_temperature') 
            ice_thickness_input = self.browser.find_element_by_name('ice_thickness')
            level_input.send_keys('12')
            time.sleep(2)
        #He should see input form for Морской пост 1 разряд category
        elif hydropost_category == 'Морской пост 1 разряд':
            level_input = self.browser.find_element_by_name('level')
            ripple_input = self.browser.find_element_by_name('ripple')
            water_temperature_input = self.browser.find_element_by_name('water_temperature')
            air_temperature_input = self.browser.find_element_by_name('air_temperature') 
            ice_thickness_input = self.browser.find_element_by_name('ice_thickness')
            level_input.send_keys('12')
            time.sleep(2)
        #He should see input form for Морской пост 2 разряд category
        elif hydropost_category == 'Морской пост 2 разряд':
            level_input = self.browser.find_element_by_name('level')
            ripple_input = self.browser.find_element_by_name('ripple')
            water_temperature_input = self.browser.find_element_by_name('water_temperature')
            air_temperature_input = self.browser.find_element_by_name('air_temperature') 
            ice_thickness_input = self.browser.find_element_by_name('ice_thickness')
            level_input.send_keys('12')
            time.sleep(2)
        #Click button for submitting observation data to database
        save_button = self.browser.find_element_by_name('save')
        save_button.click()
        time.sleep(2)
        success_alert = self.browser.find_element_by_css_selector('div.alert.alert-success')



    def test_hydrologist_can_login_have_access_only_to_his_stations_and_submit_data(self):
        #Hydrologist enter to hydrological web-site
        self.browser.get(self.live_server_url)
        #Hydrologist should be sure that he visits hydrological web-site
        self.assertEqual('Департамент гидрологии', self.browser.title)
        self.assertRegex(self.browser.current_url, '/login')
        #Hydrologist enter wrong password
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        username.send_keys('Didar')
        password.send_keys('123456')
        time.sleep(1)
        loginButton = self.browser.find_element_by_name('login')
        time.sleep(1)
        loginButton.click()
        #Browser stays on home page with login form
        self.assertRegex(self.browser.current_url, '/login')
        #Page contains error message
        errorMessage = self.browser.find_element_by_class_name('alert')
        self.assertEqual('Неправильный логин или пароль', errorMessage.text)
        #Hydrologist enter correct password
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        username.clear()
        password.clear()
        time.sleep(1)
        username.send_keys('Didar')
        password.send_keys('password')
        time.sleep(1)
        loginButton = self.browser.find_element_by_name('login')
        time.sleep(1)
        loginButton.click()
        #Hydrologist figure out that he succesfully logged in
        #His link has been changed
        time.sleep(1)
        self.assertRegex(self.browser.current_url, '/')
        #Hydrologist see his user name
        username = self.browser.find_element_by_tag_name('h1')
        time.sleep(1)
        self.assertEqual('Наблюдатель: Didar', username.text)
        #Hydrologist choose observation date        
        datepicker = self.browser.find_element_by_id('datepicker')
        datepicker.click()
        time.sleep(1)
        #He choose today date
        today_datepicker = self.browser.find_element_by_css_selector('.ui-datepicker-today')
        today_datepicker.click()
        time.sleep(1)
        #Hydrologists should see his own list of stations 
        ##We check posts,that observed by Didar
        self.checkForRowInListTable('Р. Силеты – Новомарковка')
        self.checkForRowInListTable('р. Есиль - г.Астана')
        self.checkForRowInListTable('Р. Урал – г. Уральск')
        self.checkForRowInListTable('Оз. Копа – г. Кокшетау')
        self.checkForRowInListTable('Вдхр. Буктырма– с. Аксуат')
        self.checkForRowInListTable('Каспийское море – Форт Шевченко')
        self.checkForRowInListTable('Каспийское море – п.Каламкас')
        #Hydrologist choose one hydropost
        self.selectHydropost('р. Есиль - г.Астана', 'Речной пост 2 разряд')
        #Hydrologist should see that he stays one the same page
        self.assertRegex(self.browser.current_url, '/')
        #Hydrologist should verify that he stays on the same page 
        self.assertRegex(self.browser.current_url, '/')
        #Hydrologist decide to enter observation data
        ##He choose Р. Силеты – Новомарковка for observation data submit
        self.submitObservationData('Р. Силеты – Новомарковка', 'Речной пост 1 разряд')
        ##He choose р. Есиль - г.Астана for observation data submit
        self.submitObservationData('р. Есиль - г.Астана', 'Речной пост 2 разряд')
        ##He choose Р. Урал – г. Уральск
        self.submitObservationData('Р. Урал – г. Уральск', 'Речной пост 3 разряд')
        ##He choose Вдхр. Буктырма– с. Аксуат
        self.submitObservationData('Вдхр. Буктырма– с. Аксуат', 'Озерный пост 1 разряд')
        ##He choose Оз. Копа – г. Кокшетау
        self.submitObservationData('Оз. Копа – г. Кокшетау', 'Озерный пост 2 разряд')
        ##He choose Каспийское море – Форт Шевченко
        self.submitObservationData('Каспийское море – Форт Шевченко', 'Морской пост 1 разряд')
        ##He choose Каспийское море – п.Каламкас
        self.submitObservationData('Каспийское море – п.Каламкас', 'Морской пост 2 разряд')
        time.sleep(1)
        self.fail('Finish Test')
