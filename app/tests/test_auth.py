import unittest
from flask import Flask
from flask_testing import TestCase
from flask_jwt_extended import JWTManager, create_access_token
from unittest.mock import patch
from werkzeug.security import generate_password_hash, check_password_hash
from api.auth import auth
from models.users import User
from db import db

class AuthTestCase(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a secure key in a real app
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(app)
        JWTManager(app)
        app.register_blueprint(auth, url_prefix='/auth')
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('models.users.User.query')
    def test_login_success(self, mock_user_query):
        mock_user = User(
            email='doougdoug@gmail.com',
            password='test',  # Correctly hash the password
            is_admin=False,
            first_name='test',
            last_name='test'
        )
        mock_user_query.filter_by.return_value.first.return_value = mock_user

        response = self.client.post('/auth/login', json={
            "email": "doougdoug@gmail.com",
            "password":'test'
        })

        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)

    @patch('models.users.User.query')
    def test_login_failure(self, mock_user_query):
        mock_user = User(
            email='test@example.com',
            password=generate_password_hash('wrongpassword'),  # Incorrect hashed password
            is_admin=True,
            first_name='test',
            last_name='test'
        )
        mock_user_query.filter_by.return_value.first.return_value = mock_user

        response = self.client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'password',
        })

        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid credentials')

    def test_protected_success(self):
        access_token = create_access_token(identity={'username': 'test@example.com', 'role': True})
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/auth/protected', headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['logged_in_as'], {'username': 'test@example.com', 'role': True})

    def test_protected_no_token(self):
        response = self.client.get('/auth/protected')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
