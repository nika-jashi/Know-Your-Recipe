from rest_framework import serializers

from apps.recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer For Recipes """

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'preparation_time_minutes', 'price', 'difficulty_level', 'created_at', 'user']
        read_only_fields = ['id', 'user', 'created_at']


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'link', 'updated_at']
        read_only_fields = RecipeSerializer.Meta.read_only_fields + ['updated_at']
