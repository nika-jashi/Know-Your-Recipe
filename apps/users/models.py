from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


class CustomUserManager(BaseUserManager):
    """ Manager For User """

    def create_user(self, email, password, **extra_fields):
        """ Create and save a User with the given email and password. """

        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """ Create and save a SuperUser with the given email and password. """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is False:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is False:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """ User In The System """

    email = models.EmailField(
        max_length=255,
        unique=True,
        error_messages={'unique': 'User With This Email Is Already Registered'})
    username = models.CharField(unique=True, max_length=38)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    COMPETENCE_LEVEL_CHOICES = (
        (0, _('Not chosen')),
        (1, _('Novice')),
        (2, _('Intermediate')),
        (3, _('Proficient')),
        (4, _('Advanced')),
        (5, _('Expert')),
    )

    competence_level = models.PositiveSmallIntegerField(
        choices=COMPETENCE_LEVEL_CHOICES,
        default=0,  # Start with 0 (Not chosen)
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def get_competence_level_display(self):
        for level, label in self.COMPETENCE_LEVEL_CHOICES:
            if level == self.competence_level:
                return label
        return None  # Return None if no match is found

    def __str__(self):
        return self.email
