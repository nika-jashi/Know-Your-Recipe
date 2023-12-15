from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.ingredients.models import Ingredient
from apps.users.tests import create_user
from apps.ingredients.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('ingredients:ingredient-list')


def detail_url(ingredient_id):
    """Create and return an ingredient detail URL."""
    return reverse('ingredients:ingredient-detail', args=[ingredient_id])


class ModelTest(TestCase):

    def test_create_ingredient(self):
        """ Test Ingredient Model """
        user = create_user(email='test@user.com', username='Testusername', password='GoodPass123')
        ingredient = Ingredient.objects.create(
            user=user,
            name='ing1'
        )
        self.assertEqual(str(ingredient), ingredient.name)


class PublicIngredientsApiTests(TestCase):
    """ Test Unauthenticated API Requests """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test Auth Is Required For Retrieving Ingredients """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """ Test Authenticated API Requests """

    def setUp(self):
        self.user = create_user(email='test@user.com', username='Testusername', password='GoodPass123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """ Test Retrieving A List Of Ingredients """

        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Vanilla')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """ Test List Of Ingredients Is Limited To Authenticated User """

        user2 = create_user(email='some@email.com', username='someusername', password='SomePassword123')
        Ingredient.objects.create(user=user2, name='salt')
        ingredient = Ingredient.objects.create(user=self.user, name='Pepper')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Cilantro')

        payload = {'name': 'Coriander'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """ Test Deleting An Ingredient """
        ingredient = Ingredient.objects.create(user=self.user, name='Lettuce')

        url = detail_url(ingredient_id=ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())
