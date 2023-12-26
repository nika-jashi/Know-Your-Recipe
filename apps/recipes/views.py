from django.http import HttpResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import requests
from apps.recipes.serializers import RecipeSerializer, RecipeDetailSerializer
from apps.utils import db_queries
from apps.utils.generate_pdf import make_pdf_api_call
from core import settings as api_settings


@extend_schema(tags=["Recipes"], parameters=[
    OpenApiParameter('tags', OpenApiTypes.STR),
    OpenApiParameter('ingredients', OpenApiTypes.STR),
    OpenApiParameter('recipe', OpenApiTypes.STR),
])
class GetAllRecipesView(APIView):
    """ View For Manage Recipe Api """

    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ Retrieve Recipes For Authenticated Users """

        try:
            tags = self.request.query_params.get('tags')
            ingredients = self.request.query_params.get('ingredients')
            recipe = self.request.query_params.get('recipe')

            all_recipes = db_queries.get_all_recipes()

            if tags:
                all_recipes = db_queries.get_all_recipes_by_tags(tags_data=tags)
            if ingredients:
                all_recipes = db_queries.get_all_recipes_by_ingredients(ingredients_data=ingredients)
            if recipe:
                all_recipes = db_queries.get_all_recipes_by_name_search(recipe_data=recipe)

            return Response(data=all_recipes, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                {'details': f'Error: {str(ex)}'}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=["Recipes"])
class DetailedRecipeView(APIView):
    serializer_class = RecipeDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        try:
            recipe = db_queries.get_recipe_by_id(pk=pk)
            if not recipe:
                return Response({'details': 'Recipe Not Found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = RecipeDetailSerializer(recipe)
        except Exception as ex:
            return Response(
                {'details': f'Error: {str(ex)}'}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_recipe(self, request, pk, partial=False):
        recipe = db_queries.get_recipe_by_id(pk=pk)
        is_owner = db_queries.get_recipe_owner(request=request, recipe_pk=pk)
        if not is_owner:
            return Response(
                {'Details': 'User Is Not The Owner Of The Recipe'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(
            instance=recipe,
            data=request.data,
            partial=partial,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        return self.update_recipe(request, pk, partial=True)

    def put(self, request, pk, *args, **kwargs):
        return self.update_recipe(request, pk)

    def delete(self, request, pk, *args, **kwargs):
        recipe = db_queries.get_recipe_by_id(pk=pk)
        is_owner = db_queries.get_recipe_owner(request=request, recipe_pk=pk)
        if not is_owner:
            return Response(
                {'Details': 'User Is Not The Owner Of The Recipe'},
                status=status.HTTP_404_NOT_FOUND
            )
        recipe.delete()
        return Response(
            {'Details': 'Recipe Was Deleted Successfully'}, status.HTTP_204_NO_CONTENT
        )


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


@extend_schema(tags=["Profile"])
class MyRecipesView(APIView):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        my_recipe_objects = db_queries.get_my_recipes(request=request)
        recipes_data = my_recipe_objects.data
        if recipes_data == 0:
            return Response(
                {'details': 'You Do Not Have Any Recipes Created'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(data=recipes_data, status=status.HTTP_200_OK)


@extend_schema(tags=["Recipes"])
class SaveRecipeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        is_healthy = api_settings.PDFENDPOINT_HEALTH_CHECK

        if not is_healthy:
            return Response({"error": "PDF Endpoint is not healthy"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        response = make_pdf_api_call(pk)

        if response.status_code == 200:
            return self.handle_successful_response(response)
        else:
            return self.handle_failed_response(response)

    def handle_successful_response(self, response):
        response_data = response.json()
        file_url = response_data.get("data", {}).get("url")

        file_content = requests.get(file_url).content

        http_response = HttpResponse(file_content, content_type='application/pdf')

        http_response[
            'Content-Disposition'] = f'attachment; filename="{response_data.get("data", {}).get("filename", "downloaded_file.pdf")}"'

        return http_response

    def handle_failed_response(self, response):
        return Response({"error": "Failed to retrieve the file"}, status=response.status_code)

