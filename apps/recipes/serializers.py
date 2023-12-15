from rest_framework import serializers

from apps.ingredients.models import Ingredient
from apps.ingredients.serializers import IngredientSerializer
from apps.recipes.models import Recipe
from apps.tags.models import Tag
from apps.tags.serializers import TagSerializer


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer For Recipes """

    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

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
            'ingredients',

        ]
        read_only_fields = [
            'id',
            'user',
            'created_at',
        ]
        write_only_fields = [
            'description',
            'link',
            'ingredients',
        ]

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = recipe.user

        for tag in tags:
            # Check if the tag already exists
            tag_obj = Tag.objects.filter(name=tag['name']).first()

            # If the tag belongs to a different user, create a new tag with the same name
            if tag_obj is None:
                tag_obj = Tag.objects.create(creator=auth_user, name=tag['name'])

            # Add the tag to the recipe if it's not already present
            if tag_obj not in recipe.tags.all():
                recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """ Handle Getting Or Creating Ingredients As Needed """
        auth_user = recipe.user
        for ingredient in ingredients:
            ingredient_obj, create = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])

        recipe = Recipe.objects.create(**validated_data)

        self._get_or_create_tags(tags=tags_data, recipe=recipe)
        self._get_or_create_ingredients(ingredients=ingredients_data, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)
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
            'ingredients',
        ]
        read_only_fields = RecipeSerializer.Meta.read_only_fields + ['updated_at']
