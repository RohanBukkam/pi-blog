import requests
import unittest
from SentimentAnalysisAPI import app

class UnitTestAnalyzer(unittest.TestCase):

    blogComment1 = {'comment':'fabulous author'}
    blogComment2 = {'comment':'Worst article ever'}
    blogComment3 = {'comment':'How can I help you'}

    #1
    def test_index_page_response(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertEqual(response.json, "Welcome to Pi-Blog")

    #2
    def test_status_code(self):
        tester = app.test_client(self)
        response_code = tester.get('/', follow_redirects=True)
        self.assertEqual(response_code.status_code, 200)

    #3
    def test_wrong_url_status_code(self):
        tester = app.test_client(self)
        response_code = tester.get('/sentiment', follow_redirects=True)
        self.assertEqual(response_code.status_code, 404)

    #4
    def test_valid_url_status_code(self):
        tester = app.test_client(self)
        response_code = tester.get('/api/sentiment/good', follow_redirects = True)
        self.assertEqual(response_code.status_code, 404)

    #5
    def test_get_method_sentiment_analysis(self):
        tester = app.test_client(self)
        response_code = tester.get('/sentiment/It was great reading this article', follow_redirects=True)
        self.assertEqual(response_code.status_code, 200)
        self.assertEqual(response_code.json, {'sentiment':'Positive'})

    #6
    def test_json_true_positive_sentiment_reponse(self):
        r = requests.post('http://127.0.0.1:5000/api/sentiment', json=UnitTestAnalyzer.blogComment1)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'sentiment': 'Positive'})

    #7
    def test_json_true_negative_sentiment_reponse(self):
        r = requests.post('http://127.0.0.1:5000/api/sentiment', json=UnitTestAnalyzer.blogComment2)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'sentiment': 'Negative'})

    #8
    def test_json_false_negative_sentiment_reponse(self):
        r = requests.post('http://127.0.0.1:5000/api/sentiment', json=UnitTestAnalyzer.blogComment3)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'sentiment': 'Negative'})

if __name__ == "__main__":
    unittest.main()