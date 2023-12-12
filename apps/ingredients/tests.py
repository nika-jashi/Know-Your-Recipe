from django.test import TestCase

from apps.ingredients.models import Ingredient
from apps.users.tests import create_user


class ModelTest(TestCase):

    def test_create_ingredient(self):
        user = create_user(email='test@user.com', username='Testusername', password='GoodPass123')
        ingredient = Ingredient.objects.create(
            user=user,
            name='ing1'
        )
