from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """ Test Creating A User With An Email Is Successful """

        email = 'test@example.com'
        first_name = 'test'
        last_name = 'user'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

    def test_new_user_email_normilized(self):
        """ Test Email Is Normalized For New users. """

        first_name = 'test'
        last_name = 'user'
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test That Creating A User Without An Email Raises A ValueError """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                first_name='test',
                last_name='user',
                password='test123')

    def test_create_superuser(self):
        """ Test Creating Superuser """

        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


CREATE_USER_URL = reverse('users:register')
TOKEN_URL = reverse('users:login')


def create_user(**params):
    """ Create And Return A New User """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """ Test The Public Features Of The User Api """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'first_name': 'normal',
            'last_name': 'user',
            'password': 'TestPass123',
            'confirm_password': 'TestPass123',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """ Test Error Returned If User With Email Exists """

        payload = {
            'email': 'test@example.com',
            'first_name': 'normal',
            'last_name': 'user',
            'password': 'TestPass123',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'first_name': 'normal',
            'last_name': 'user',
            'password': 'test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test Generates Token For Valid Credentials """

        user_details = {
            'email': 'test@example.com',
            'first_name': 'normal',
            'last_name': 'user',
            'password': 'TestPass123',
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """ Test Returns Error If Credentials Invalid """

        user_details = {
            'email': 'test@example.com',
            'first_name': 'normal',
            'last_name': 'user',
            'password': 'TestPass123',
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': 'bad-pass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        """ Test Posting A Blank Password Returns An Error """
        user_details = {
            'email': 'test@example.com',
            'first_name': 'normal',
            'last_name': 'user',
            'password': 'TestPass123',
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
