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
                    MinLengthValidator(8)],
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        max_length=255,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password', 'confirm_password']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError(
                {"confirm_password": _("[Password] and [Confirm Password] Don't Match.")}
            )

        del data['confirm_password']  # deleting confirm_password because we only need it for verification
        return data

    def create(self, validated_data):
        """ Create And Return A User With Encrypted Password """

        return get_user_model().objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer To View Users Profile and Update It """

    email = serializers.EmailField(read_only=True)
    date_joined = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'competence_level',
            'date_joined'
        ]

        extra_kwargs = {
            'first_name': {'min_length': 3},
            'last_name': {'min_length': 3},
            'username': {'min_length': 3}
        }

    def validate(self, data):
        competence_level = data.get('competence_level')
        if competence_level is not None and (competence_level < 0 or competence_level > 5):
            raise serializers.ValidationError("Competence level must be between 0 and 5.")

        return data

    def update(self, instance, validated_data):
        user = super().update(instance=instance, validated_data=validated_data)
        user.save()
        return user


class UserChangePasswordSerializer(serializers.Serializer):  # noqa
    """A serializer for user to change password when authenticated. Includes all the required
       fields and validations, plus a repeated password. """

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[does_not_contains_whitespace,
                    contains_uppercase,
                    contains_digits,
                    contains_lowercase,
                    MinLengthValidator(8)])
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = self.context.get('request').user
        if not user.check_password(data.get("old_password")):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"new_password": "[New Password] and [Confirm Password] Don't Match."}
            )

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance
