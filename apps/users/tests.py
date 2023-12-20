from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:register')
TOKEN_URL = reverse('users:login')
PROFILE_URL = reverse('users:profile')
PASSWORD_CHANGE_URL = reverse('users:password-change')


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """ Test Creating A User With An Email Is Successful """

        email = 'test@example.com'
        username = 'user'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.username, username)

    def test_new_user_email_normilized(self):
        """ Test Email Is Normalized For New users. """

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com', 'asda'],
            ['Test2@Example.com', 'Test2@example.com', 'dsaas'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com', 'afsdg'],
            ['test4@example.COM', 'test4@example.com', 'adfgds'],
        ]
        for email, expected, username in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                username=username,
                password='sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test That Creating A User Without An Email Raises A ValueError """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                username='user',
                password='test123')

    def test_create_superuser(self):
        """ Test Creating Superuser """

        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


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
            'username': 'user',
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
            'username': 'user',
            'password': 'TestPass123',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'username': 'user',
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
            'username': 'user',
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
            'username': 'user',
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
            'username': 'user',
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

    def test_retrieve_user_unauthorized(self):
        """ Test Authentication Is Required For Users """

        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiUserTests(TestCase):
    """ Test API Requests That Require Authentication """

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            competence_level=0,
            username='user',
            password='TestPass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ Test Retrieving Profile For Logged In User """

        res = self.client.get(PROFILE_URL)
        profile_picture_value = self.user.profile_picture

        # Check if the ImageField is empty
        profile_picture_data = None
        if profile_picture_value:
            profile_picture_data = profile_picture_value.name

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'competence_level': self.user.competence_level,
            'date_joined': self.user.date_joined.strftime('%Y-%m-%d'),
            'profile_picture': profile_picture_data
        })

    def test_post_profile_not_allowed(self):
        """ Test POST Is Not Allowed For The Profile Endpoint """

        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test Updating The User Profile For Authenticated User """

        payload = {
            'username': 'updated_username',
            'first_name': 'updated_first_name',
            'last_name': 'updated_last_name',
            'competence_level': 0,

        }

        res = self.client.patch(PROFILE_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.username, payload['username'])
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])
        self.assertEqual(self.user.competence_level, payload['competence_level'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_user_password(self):
        """ Test Updating The User Password For Authenticated User """
        payload = {
            'old_password': 'TestPass123',
            'new_password': 'BetterTestPass123',
            'confirm_password': 'BetterTestPass123',
        }
        res = self.client.post(PASSWORD_CHANGE_URL, payload)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['new_password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
