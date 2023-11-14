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

    def get_object(self, pk):  # noqa
        try:
            return db_queries.get_recipe_by_id(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404('Recipe Not Found')

    def get(self, request, pk, *args, **kwargs):
        try:
            recipe = self.get_object(pk=pk)
            serializer = RecipeDetailSerializer(recipe)
        except Exception as ex:
            return Response({'details': f'Error: {str(ex)}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        recipe = self.get_object(pk=pk)
        serializer = RecipeDetailSerializer(instance=recipe, data=request.data, partial=True)
        is_owner = db_queries.get_recipe_owner(request=request, recipe_pk=pk)
        if not is_owner:
            return Response({"Detail": "User Is Not The Owner Of Recipe"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Recipes"])
class CreateRecipeView(APIView):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
