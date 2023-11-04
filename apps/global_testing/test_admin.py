from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """ Tests For Django Admin """

    def setUp(self):
        """ Create User And Client """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            first_name='admin',
            last_name='superuser',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            first_name='basic',
            last_name='user',
            password='testpass123',
        )

    def test_users_list(self):
        """ Test That users Are Listed On Page """
        url = reverse(viewname='admin:users_customuser_changelist')  # noqa
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)

    def test_edit_user_page(self):
        """ Test The Edit User Page Works """

        url = reverse(
            viewname='admin:users_customuser_change',
            args=[self.user.id]
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test The Create User Page Works """

        url = reverse('admin:users_customuser_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
