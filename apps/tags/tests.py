from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.users.tests import create_user
from apps.tags.models import Tag
from apps.tags.serializers import TagSerializer


TAGS_URL = reverse('tags:tag-list')


class PrivateTagTests(TestCase):
    """ Tests For Tags Module """

    def setUp(self):
        user = create_user(
            email='user@example.com',
            username='user',
            password='Testpass123'
        )
        self.user = user
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_auth_required(self):
        """ Test Auth Is Required For Retrieving Tags """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tag(self):
        tag = Tag.objects.create(user=self.user, name='tag1')

        self.assertEqual(str(tag), tag.name)

    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('recipe_count')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
