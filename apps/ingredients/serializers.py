from rest_framework import serializers

from apps.ingredients.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer For Ingredients """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
