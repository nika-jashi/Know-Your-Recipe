from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.recipes.models import Recipe
from apps.recipes.serializers import RecipeSerializer, RecipeDetailSerializer
from apps.utils import db_queries


@extend_schema(tags=["Recipes"])
class GetAllRecipesView(APIView):
    """ View For Manage Recipe Api """
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ Retrieve Recipes For Authenticated Users """
        try:
            all_recipes = db_queries.get_all_recipes()
            recipes_data = all_recipes.data
            return Response(data=recipes_data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'details': f'Error: {str(ex)}'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Recipes"])
class DetailedRecipeView(APIView):
    serializer_class = RecipeDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return db_queries.get_recipe_by_id(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        try:
            recipe = self.get_object(pk=pk)
            return Response(recipe.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'details': f'Error: {str(ex)}'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Recipes"])
class CreateRecipeView(APIView):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = RecipeSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
