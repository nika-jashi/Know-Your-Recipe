from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import CustomUser
from apps.users.serializers import UserSerializer


@extend_schema(tags=["Auth"])
class UserRegistrationView(APIView):
    """ A view for creating new users. with POST request method and proper status codes """

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
