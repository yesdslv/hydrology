from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import unittest

import time

from hydrology.models import Hydropost, Hydrologist, Observation

class VisitorLoginTest(LiveServerTestCase):
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
        ##Оз. Копа – г. Кокшетау
        ##ОГП-2
        thirdHydropost = Hydropost.objects.get(code = 11919)
        ##Didar will enter data for these hydroposts
        Observation.objects.create(hydropost = firstHydropost,
                            hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = secondHydropost,
                            hydrologist = new_hydrologist)
        Observation.objects.create(hydropost = thirdHydropost,
                            hydrologist = new_hydrologist)
        

    def tearDown(self):
        self.browser.quit()

    def checkForRowInListTable(self, rowText):
        table = self.browser.find_element_by_name('hydropost')
        rows = table.find_elements_by_tag_name('option')
        self.assertIn(rowText, [row.text for row in rows])

    def selectHydropost(self, hydropost_name):
        #Hydrologist select one hydropost
        select = Select(self.browser.find_element_by_name('hydropost'))
        select.select_by_visible_text(hydropost_name)
        button = self.browser.find_element_by_name('asput')
        #Hydrologist should see hydropost category in header h2
        ##That one is for testing get request 
        ##We get hydropost category
        hydropost_category_header = self.browser.find_element_by_tag_name('h2')
        self.assertEqual('Речной пост 1 разряд', hydropost_category_header.text)
        #Hydrologist press OK button
        button.click()


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
        time.sleep(2)
        self.assertEqual('Didar', username.text)
        #Hydrologists should see his own list of stations 
        ##We check posts,that observed by Didar
        self.checkForRowInListTable('Р. Силеты – Новомарковка')
        self.checkForRowInListTable('р. Есиль - г.Астана')
        self.checkForRowInListTable('Оз. Копа – г. Кокшетау')
        #Hydrologist choose one hydropost
        self.selectHydropost('Р. Силеты – Новомарковка')
        #Hydrologist should see that he is redirected to page for data submitting
        self.assertRegex(self.browser.current_url, '/record')
        #Hydrologist should see hydropost name in header
        time.sleep(5)
        hydropost_name_header = self.browser.find_element_by_tag_name('h1')
        post_category_header = self.browser.find_element_by_tag_name('h2')
        self.assertEqual('Р. Силеты – Новомарковка', hydropost_name_header.text)
        self.assertEqual('Речной пост 1 разряд', post_category_header.text)
        #Hydrologist should see forms supplied for this hydropost category
        level_input = self.browser.find_element_by_name('level')
        discharge_input = self.browser.find_element_by_name('discharge')
        water_temperature_input = self.browser.find_element_by_name('water_temperature')
        air_temperature_input = self.browser.find_element_by_name('air_temperature')
        time.sleep(8)
        #Hydrologist press back button
        self.browser.back()
        time.sleep(5)
        #Hydrologist select another hydropost
        self.selectHydropost('Оз. Копа – г. Кокшетау')
        #Hydrologist should see hydropost name in header
        time.sleep(5)
        hydropost_name_header = self.browser.find_element_by_tag_name('h1')
        post_category_header = self.browser.find_element_by_tag_name('h2')
        self.assertEqual('Оз. Копа – г. Кокшетау', hydropost_name_header.text)
        self.assertEqual('Озерный пост 2 разряд', post_category_header.text)
        #Hydrologist should see forms supplied for this hydropost category
        level_input = self.browser.find_element_by_name('level')
        water_temperature_input = self.browser.find_element_by_name('water_temperature')
        air_temperature_input = self.browser.find_element_by_name('air_temperature')
        ripple_input = self.browser.find_element_by_name('ripple')         
        time.sleep(3)
        self.fail('Finish Test')
