from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.ingredients.serializers import IngredientSerializer
from apps.utils import db_queries


@extend_schema(tags=["Profile"])
class GetAllIngredientsView(APIView):
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        my_ingredients_objects = db_queries.get_my_ingredients(request=request)
        ingredients_data = my_ingredients_objects.data
        if ingredients_data == 0:
            return Response(
                {'details': 'You Do Not Have Any Ingredients Created'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(data=ingredients_data, status=status.HTTP_200_OK)
