from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import (
    UserSerializer,
    UserProfileSerializer, UserChangePasswordSerializer
)
from apps.utils.db_queries import check_user_exists


@extend_schema(tags=["Auth"],
               responses={
                   status.HTTP_201_CREATED: UserSerializer,
                   status.HTTP_400_BAD_REQUEST: UserSerializer,
               })
class UserRegistrationView(APIView):
    """ A view for creating new users. with POST request method and proper status codes """

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Auth"],
               responses={
                   status.HTTP_200_OK: TokenObtainPairSerializer,
                   status.HTTP_400_BAD_REQUEST: 'Bad Request',
                   status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
               })
class AccountLoginView(TokenObtainPairView):
    """View for user to log in using JWT bearer Token"""

    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs) -> Response:
        email = request.data.get("email")
        if not check_user_exists(email=email):
            return Response(
                data={"detail": "No Active User Found With The Given Credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)


@extend_schema(tags=["Profile"])
class AccountProfileView(APIView):
    """ View For User To See Their Profile """

    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs) -> Response:
        """ GET Method For Users To View Their Profile """

        current_user = request.user
        serializer = UserProfileSerializer(instance=current_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs) -> Response:
        """ PATCH Method For Users To Update Their Profile """

        current_user = request.user
        serializer = UserProfileSerializer(instance=current_user, data=request.data, partial=True)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Profile"])
class UserChangePasswordView(APIView):
    """View for user to change password when authenticated"""

    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request) -> Response:
        current_user = request.user
        serializer = self.serializer_class(
            instance=current_user, data=request.data, context={"request": request}
        )
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response({"detail": "You successfully changed your password."}, status=status.HTTP_200_OK)
