from rest_framework import serializers

from apps.recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer For Recipes """

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time_minutes', 'price', 'difficulty_level']
