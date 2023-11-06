from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.utils.custom_validators import (does_not_contains_whitespace,
                                          contains_uppercase,
                                          contains_digits,
                                          contains_lowercase)


class UserSerializer(serializers.ModelSerializer):
    """ Serializer For The User Object """

    password = serializers.CharField(
        max_length=255,
        write_only=True,
        validators=[does_not_contains_whitespace,
                    contains_uppercase,
                    contains_digits,
                    contains_lowercase,
                    MinLengthValidator(8)]
    )
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']

        extra_kwargs = {
            'first_name': {'min_length': 3},
            'last_name': {'min_length': 3},
        }

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError(
                {"confirm_password": _("[Password] and [Confirm Password] Don't Match.")}
            )

        del data['confirm_password']  # deleting confirm_password because we don't use it after validation

        return data

    def create(self, validated_data):
        """ Create And Return A User With Encrypted Password """

        return get_user_model().objects.create_user(**validated_data)
