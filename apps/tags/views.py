from django.shortcuts import render
from django.http import Http404
from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.tags.serializers import TagSerializer
from apps.utils import db_queries


@extend_schema(tags=["Tags"])
class GetAllRecipesView(APIView):
    """ View For Manage Recipe Api """

    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ Retrieve Recipes For Authenticated Users """

        try:
            all_tags = db_queries.get_all_tags()
            recipes_data = all_tags.data
            return Response(data=recipes_data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                {'details': f'Error: {str(ex)}'}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=["Tags"])
class CreateTagView(APIView):
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
