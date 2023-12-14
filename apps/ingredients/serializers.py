from django.db import IntegrityError
from rest_framework import serializers

from apps.ingredients.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer For Ingredients """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name']

    def create(self, validated_data):
        ingredient_name = validated_data['name']
        user = validated_data['user']
        try:
            return super().create(validated_data)
        except IntegrityError:
            existing_ingredient = Ingredient.objects.get(user=user, name=ingredient_name)
            return existing_ingredient
