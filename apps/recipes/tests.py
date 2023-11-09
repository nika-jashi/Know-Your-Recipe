from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.recipes.models import Recipe
from apps.users.tests import create_user
from apps.recipes.serializers import RecipeSerializer

RECIPES_URL = reverse('recipes:recipe-list')


def create_recipe(user, **params):
    """ Create And Return A Sample Recipe """
    defaults = {
        'title': "Sample recipe title",
        'preparation_time_minutes': 5,
        'price': Decimal('12.5'),
        'description': "Sample recipe description",
        'link': "https://example.com/recipe.pdf",
        'difficulty_level': 0,
    }
    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicApiRecipeTest(TestCase):
    """ Test Unauthenticated API Requests """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiRecipeTests(TestCase):
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
            description='Sample recipe Description',
            preparation_time_minutes=5,
            price=Decimal('5.50'),
            link='asd',
            difficulty_level=0,
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_retrieve_recipes(self):
        """ Test Retrieving A List Of Recipes """

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
