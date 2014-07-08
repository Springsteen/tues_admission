from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest 

class FunctionalTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.get('localhost:8000')

	def tearDown(self):
		self.browser.quit()

class TestHomePage(FunctionalTest):

	def test_login_redirects_to_login_page(self):
		pass

if __name__ == '__main__':
	unittest.main(warnings='ignore')