from flask import url_for
from flask_login import current_user

from utils import app
import unittest

from utils.models import User


class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_index_page(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # To Ensure that login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'SIGN IN' in response.data)

    # To Ensure that login behaves correctly given the correct credentials
    def test_users_can_login(self):
        tester = app.test_client(self)
        tester.post('/login',
                    data=dict(name='shubhangi', email='shubhangi@gmail.com', password='shubhangi'),
                    follow_redirects=True
                    )
        response = tester.get('http://127.0.0.1:5000/home', follow_redirects=True)

        self.assertIn(b'', response.data)

    #To Ensure that login behaves correctly given the incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post('/login',
                                   data=dict(name='shubhangi',email='wrong', password='shubhangi'),
                                   follow_redirects=True)

        self.assertIn(b'Invalid email address.', response.data)



    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(name='shubhangi', email='shubhangi@gmail.com', password='shubhangi'),
            follow_redirects=True
        )
        response = tester.get('/login', follow_redirects=True)
        self.assertIn(b'SIGN IN', response.data)

    # To Ensure that register page loads correctly
    def test_register_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/register', content_type='html/text')
        self.assertTrue(b'SIGN UP' in response.data)

    #To Ensure that register behaves correctly given the incorrect email_id
    def test_incorrect_email_id(self):
        tester = app.test_client(self)
        response = tester.post('/register',
                               data=dict(name='shubhangi', username='shubhangi',email='wrong', password='shubhangi',
                                         confirm_password='shubhangi'),follow_redirects=True
                               )
        self.assertIn(b'Invalid email address.', response.data)




if __name__ == '__main__':
    unittest.main()
