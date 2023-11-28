from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.recipes.models import Recipe
from apps.users.tests import create_user
from apps.recipes.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer
)
from apps.tags.models import Tag

RECIPES_URL = reverse('recipes:recipe-list')
RECIPE_CREATE_URL = reverse('recipes:recipe-create')


def detail_url(recipe_id):
    """ Create And Return A Recipe Detail Url """
    return reverse('recipes:recipe-detail', args=[recipe_id])


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

    def test_create_recipe_is_successful(self):
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

    def test_get_recipe_detail(self):
        """ Test Get Recipe Detail """
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """ Test Creating A Recipe """
        payload = {
            'title': "Sample recipe title",
            'preparation_time_minutes': 5,
            'price': Decimal('12.5'),
            'difficulty_level': 0,
        }

        res = self.client.post(RECIPE_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        uid = res.data['id']
        recipe = Recipe.objects.get(id=uid)
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """ Test Partial Update Of A Recipe """
        original_link = 'original_link'
        recipe = create_recipe(
            user=self.user,
            title='sample recipe title',
            link=original_link
        )
        payload = {
            'title': 'New Recipe Title'
        }
        url = detail_url(recipe_id=recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """ Test Full Update Of Recipe """

        recipe = create_recipe(
            user=self.user,
            title='Sample recipe name',
            description='Sample recipe Description',
            preparation_time_minutes=5,
            price=Decimal('5.50'),
            link='sample link',
            difficulty_level=0,
        )

        payload = {
            'title': 'new title',
            'description': 'new desc',
            'preparation_time_minutes': 10,
            'price': Decimal('2.5'),
            'link': 'new link',
            'difficulty_level': 2,
        }
        url = detail_url(recipe_id=recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)

        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """ Test Changing The Recipe User Results In An Error """
        new_user = create_user(
            email='user2@example.com',
            username='username2',
            password='Password123'
        )
        recipe = create_recipe(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(recipe_id=recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """ Test Deleting A Recipe Successful """

        recipe = create_recipe(user=self.user)

        url = detail_url(recipe_id=recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_users_recipe_error(self):
        """ Test Trying To Delete Another Users Recipe Gives Error """
        new_user = create_user(
            email='user2@example.com',
            username='username2',
            password='Testpass2'
        )
        recipe = create_recipe(user=new_user)
        url = detail_url(recipe_id=recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_new_tags(self):
        """ Test Creating A Recipe With New Tags """

        recipe = create_recipe(
            user=self.user,
            title='Sample recipe name',
            description='Sample recipe Description',
            preparation_time_minutes=5,
            price=Decimal('5.50'),
            link='sample link',
            difficulty_level=0,
            tags=[
                {'name': 'Thai'},
                {'name': 'Dinner'},
            ]
        )
        res = self.client.post(RECIPE_CREATE_URL, recipe, format='json')  # noqa

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe_object = recipes[0]
        self.assertEqual(recipe_object.tags.count(), 2)
        for tag in recipe['tags']:
            exists = recipe_object.tags.filter(
                name=tag['name'],
                user=self.user
            ).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_tags(self):
        """ Test Creating A Recipe With Existing Tag """
        tag_indian = Tag.objects.create(creator=self.user, name='Indian')
        payload = create_recipe(
            user=self.user,
            title='Sample recipe name',
            description='Sample recipe Description',
            preparation_time_minutes=5,
            price=Decimal('5.50'),
            link='sample link',
            difficulty_level=0,
            tags=[
                {'name': 'Indian'},
                {'name': 'Breakfast'},
            ]
        )
        res = self.client.post(RECIPE_CREATE_URL, payload, format='json')  # noqa
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)
        self.assertIn(tag_indian, recipe.tags.all())
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)
