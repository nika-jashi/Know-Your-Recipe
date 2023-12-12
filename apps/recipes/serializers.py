from rest_framework import serializers

from apps.recipes.models import Recipe
from apps.tags.models import Tag
from apps.tags.serializers import TagSerializer


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

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = recipe.user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                creator=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

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

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """ Serializer For Recipe Details """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + [
            'description',
            'link',
        ]
        read_only_fields = RecipeSerializer.Meta.read_only_fields + ['updated_at']
