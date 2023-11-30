from rest_framework import serializers

from apps.recipes.models import Recipe
from apps.tags.serializers import TagSerializer
from apps.tags.models import Tag


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer For Recipes """

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'preparation_time_minutes',
            'price',
            'difficulty_level',
            'created_at',
            'user',
            'tags',

        ]
        read_only_fields = [
            'id',
            'user',
            'created_at',
        ]
        write_only_fields = [
            'description',
            'link',
        ]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        current_user = validated_data['user']
        tags = []

        for tag_data in tags_data:
            tag_serializer = TagSerializer(data=tag_data)
            tag_serializer.is_valid(raise_exception=True)
            tag_obj = tag_serializer.save(creator=current_user)
            tags.append(tag_obj)

        recipe.tags.set(tags)
        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """ Serializer For Recipe Details """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + [
            'description',
            'link',
        ]
        read_only_fields = RecipeSerializer.Meta.read_only_fields + ['updated_at']
