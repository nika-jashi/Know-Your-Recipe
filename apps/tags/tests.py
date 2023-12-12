from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.users.tests import create_user
from apps.tags.models import Tag
from apps.tags.serializers import TagSerializer

TAGS_URL = reverse('tags:tag-list')


def detail_url(tag_id):
    """ Create And Return A Tag Detail Url """
    return reverse('tags:tag-detail', args=[tag_id])


class PublicApiRecipeTest(TestCase):
    """ Test Unauthenticated API Requests """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test Auth Is Required For Retrieving Tags """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


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

    def test_create_tag(self):
        tag = Tag.objects.create(creator=self.user, name='tag1')

        self.assertEqual(str(tag), tag.name)

    def test_retrieve_tags(self):
        Tag.objects.create(creator=self.user, name='Vegan')
        Tag.objects.create(creator=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-created_at')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_detail_tag(self):
        """ test Viewing Tag Details """
        tag = Tag.objects.create(
            creator=self.user,
            name='Dinner',
            description='This is for tests only'
        )
        url = detail_url(tag_id=tag.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_tag(self):
        """ Test Deleting A Tag Successful """
        tag = Tag.objects.create(
            creator=self.user,
            name='Breakfast',
            description='test desc'
        )

        url = detail_url(tag_id=tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(pk=tag.id)
        self.assertFalse(tags.exists())
