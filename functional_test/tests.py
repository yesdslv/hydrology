from django.test import LiveServerTestCase

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

import unittest

import time

class VisitorLoginTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_user_can_login_and_have_access_only_to_his_stations(self):
        #Hydrologist enter to hydrological web-site
        self.browser.get(self.live_server_url)
        #Hydrologist should be sure that he visits hydrological web-site
        self.assertEqual('Гидрологические наблюдения', self.browser.title)
        time.sleep(3)
        #Hydrologist enter wrong password
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        username.send_keys('Didar')
        password.send_keys('123456')
        time.sleep(3)
        loginButton = self.browser.find_element_by_name('login')
        loginButton.click()
        #Browser stays on home page with login form
        self.assertEqual(self.browser.current_url, '/')
        #Page contains error message
        errorParagraph = self.browser.find_element_by_tag_name('p')
        self.assertIn('Неправильный логин или пароль', errorParagraph)
        #Hydrologist enter correct password
        username = self.browser.find_element_by_name('username')
        password = self.browser.find_element_by_name('password')
        username.send_keys('Didar')
        password.send_keys('fjytgh567')
        time.sleep(3)
        loginButton = self.browser.find_element_by_name('login')
        loginButton.click()
        #Hydrologist figure out that he succesfully logged in
        #His link has been changed
        self.assertEqual(self.browser.current_url, '/index')
        self.fail('Finish Test')
