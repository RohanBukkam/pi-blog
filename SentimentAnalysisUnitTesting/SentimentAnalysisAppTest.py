#This file is for testing purpose only.
#This file has been moved to a subfolder for better structure of repository.
#It will run without any errors when run through parent folder where SentimentAnalysisTrialApp.py and other files are located.

from SentimentAnalysisTrialApp import app #Otherwise this import will throw an error.
import unittest
import json

class UnitTestAnalyzer(unittest.TestCase):

    def test_status_code(self):
        tester = app.test_client(self)
        response_code = tester.get('/', follow_redirects=True)
        self.assertEqual(response_code.status_code, 200)


    def test_wrong_url_status_code(self):
        tester = app.test_client(self)
        response_code = tester.get('/sentiment', follow_redirects=True)
        self.assertEqual(response_code.status_code, 404)


    def test_valid_url_status_code(self):
        tester = app.test_client(self)
        response_code = tester.get('/sentiment/good', follow_redirects = True)
        self.assertEqual(response_code.status_code, 200)


    def test_index_page_response(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertEqual(response.data, b'Welcome to Pi-Blog')


    def test_true_positive_sentiment_reponse(self):
        tester = app.test_client(self)
        response = tester.get('/sentiment/awesome day', follow_redirects=True)
        self.assertEqual(response.data, b'Positive')


    def test_true_negative_sentiment_reponse(self):
        tester = app.test_client(self)
        response = tester.get('/sentiment/this is disgusting', follow_redirects=True)
        self.assertEqual(response.data, b'Negative')


    def test_false_positive_sentiment_response(self):
        tester = app.test_client(self)
        response = tester.get('/sentiment/help me', follow_redirects=True)
        self.assertEqual(response.data, b'Positive')


    def test_true_positive_sentiment_reponse2(self):
        tester = app.test_client(self)
        response = tester.get('/sentiment/This blog seems to be super realistic', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.data, b'Positive')


if __name__ == "__main__":
    unittest.main()
