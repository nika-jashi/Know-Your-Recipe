from rest_framework import serializers

from apps.recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer For Recipes """
    created_at = serializers.DateTimeField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'preparation_time_minutes', 'price', 'difficulty_level', 'created_at']


class RecipeDetailSerializer(RecipeSerializer):
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + [
            'updated_at', 'link', 'user'
        ]