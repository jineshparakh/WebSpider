'''
Importing the necessary libraries and the flask app for testing
'''
from app import app
import unittest
from flask_testing import TestCase

class FlaskTestcase(unittest.TestCase):

    #set up the app
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False #if this is true then the forms do not get submitted during local testing
        self.app = app.test_client()
        self.assertEqual(app.debug, False) 
        self.assertEqual(app.testing, True)
    
    #test if the index page is loading or not 
    def test_index(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Enter URL to start crawling: ', response.data) #checking if the correct page has loaded
        self.assertEqual(response.status_code, 200)
    #function to post forms
    def post_form(self, url, levels):
        return self.app.post(
            '/',
            data=dict(url=url, levels=levels),
            follow_redirects=True
        )
    #test the form when a valid URL and valid Max Level are given    
    def test_valid_URL_form(self):
        response = self.app.post(
            '/',
            data=dict(url='https://www.google.com', levels=1),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bigram Cloud', response.data)

    #give invalid level to test
    def test_invalid_Level_form(self):
        response = self.post_form('https://www.google.com', 3)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a value between 1 and 2', response.data)    

    #invalid URL to test
    def test_invalid_URL_form_2(self):
        response = self.post_form('https://om', 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid Base URL', response.data)  

if __name__=="__main__":
    unittest.main()        