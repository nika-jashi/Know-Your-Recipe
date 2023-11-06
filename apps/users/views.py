from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import UserSerializer
from apps.utils.db_queries import find_existing_user


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


@extend_schema(tags=["Auth"])
class AccountLoginView(TokenObtainPairView):
    """View for user to log in using JWT bearer Token"""

    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not find_existing_user(email=email):
            return Response(
                {"detail": "No Active User Found With The Given Credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
