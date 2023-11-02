from django.test import TestCase
from django.contrib.auth import get_user_model


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
        """ Test Email Is Normalized For New Users. """

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
            get_user_model().objects.create_user(email='', first_name='test', last_name='user', password='test123')

    def test_create_superuser(self):
        """ Test Creating Superuser """

        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
