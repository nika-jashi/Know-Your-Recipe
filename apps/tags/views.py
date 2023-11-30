from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.tags.serializers import TagSerializer, TagDetailSerializer
from apps.utils import db_queries


@extend_schema(tags=["Tags"])
class GetAllTagsView(APIView):
    """ View For Manage Tag Api """

    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """ Retrieve Tags For Authenticated Users """

        try:
            all_tags = db_queries.get_all_tags()
            tags_data = all_tags.data
            return Response(data=tags_data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                {'details': f'Error: {str(ex)}'}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=["Tags"])
class DetailedTagView(APIView):
    """ Detail View For Tags To View Them  Update And Delete """

    serializer_class = TagDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        try:
            tag = db_queries.get_tag_by_id(pk=pk)
            if not tag:
                return Response({'details': 'Tag Not Found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = TagDetailSerializer(tag)
        except Exception as ex:
            return Response(
                {'details': f'Error: {str(ex)}'}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_tag(self, request, pk, partial=False):
        """ Method To Manage Tag Update """
        tag = db_queries.get_tag_by_id(pk=pk)
        is_owner = db_queries.get_tag_owner(request=request, tag_pk=pk)
        if not is_owner:
            return Response(
                {'Details': 'User Is Not The Owner Of The Tag'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(
            instance=tag,
            data=request.data,
            partial=partial
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        """ View To Update Tag Partially """

        return self.update_tag(request, pk, partial=True)

    def put(self, request, pk, *args, **kwargs):
        """ View To Update Tag Fully """

        return self.update_tag(request, pk)

    def delete(self, request, pk, *args, **kwargs):
        """ Method To Delete Tag """

        tag = db_queries.get_tag_by_id(pk=pk)
        is_owner = db_queries.get_tag_owner(request=request, tag_pk=tag.pk)
        if not is_owner:
            return Response(
                {'Details': 'User Is Not The Owner Of The Tag'},
                status=status.HTTP_404_NOT_FOUND
            )
        tag.delete()
        return Response(
            {'Details': 'Tag Was Deleted Successfully'}, status.HTTP_204_NO_CONTENT
        )


@extend_schema(tags=["Tags"])
class CreateTagView(APIView):
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(creator=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Profile"])
class MyTagsView(APIView):
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        my_tags_objects = db_queries.get_my_tags(request=request)
        tags_data = my_tags_objects.data
        if tags_data == 0:
            return Response(
                {'details': 'You Do Not Have Any Tags Created'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(data=tags_data, status=status.HTTP_200_OK)
