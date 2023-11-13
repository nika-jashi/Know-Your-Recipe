from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.recipes.serializers import RecipeSerializer, RecipeDetailSerializer
from apps.utils.db_queries import get_all_recipes


@extend_schema(tags=["Recipes"])
class GetAllRecipes(APIView):
    """ View For Manage Recipe Api """
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ Retrieve Recipes For Authenticated Users """
        all_recipes = get_all_recipes()
        serializer = RecipeSerializer(data=all_recipes, many=True)
        if not serializer.is_valid(raise_exception=True):
            return Response({'details': "Error"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
