from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from apps.users.serializers import UserSerializer


class UserRegistrationView(CreateAPIView):
    """ Create A New User In The System """

    serializer_class = UserSerializer
