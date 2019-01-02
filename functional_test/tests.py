from selenium import webdriver

import unittest

import time

class NewVisitorTest(unittest.TestCase):
	def setUp():
		self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)
	def tearDown():
		self.browser.quit()

	def test_django_is_started(self):
		self.browser.get('http://localhost:8000')
		self
		time.sleep(3)	
		self.fail('Finish test')		

if __name__ == '__main__':
	unittest.main()		
