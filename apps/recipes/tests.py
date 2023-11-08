from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from apps.recipes.models import Recipe
from apps.users.tests import create_user


class PrivateApiTests(TestCase):
    """ Test API Requests That Require Authentication """

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            username='user',
            password='TestPass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_recipe(self):
        """ Test Creating A recipe Is Successful """

        recipe = Recipe.objects.create(
            user=self.user,
            title='Sample recipe name',
            preparation_time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe Description'
        )

        self.assertEqual(str(recipe), recipe.title)

