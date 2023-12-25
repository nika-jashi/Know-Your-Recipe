import uuid
import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.ingredients.models import Ingredient
from core import settings
from apps.tags.models import Tag


def recipe_image_file_path(instance, filename):
    """ Generate file path for new recipe image """
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class Recipe(models.Model):
    """ Recipe Object """
    DIFFICULTY_CHOICES = [
        (0, _('Not chosen')),
        (1, _('Novice')),
        (2, _('Intermediate')),
        (3, _('Advanced')),
    ]

    title = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    preparation_time_minutes = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(Ingredient)
    image = models.ImageField(upload_to=recipe_image_file_path)

    difficulty_level = models.PositiveSmallIntegerField(
        choices=DIFFICULTY_CHOICES,
        default=0,  # Start with 0 (Not chosen)
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def convert_minutes_to_hours_and_minutes(self):
        if self.preparation_time_minutes < 0:
            raise ValueError("Minutes must be a non-negative integer.")

        hours = self.preparation_time_minutes // 60
        remaining_minutes = self.preparation_time_minutes % 60

        if hours == 0:
            return f"{remaining_minutes} minutes"
        elif remaining_minutes == 0:
            return f"{hours} hours"
        else:
            return f"{hours} hours and {remaining_minutes} minutes"

    def get_competence_level_display(self):
        for level, label in self.DIFFICULTY_CHOICES:
            if level == self.difficulty_level:
                return label
        return None  # Return None if no match is found

    def clean(self):
        # Check if the number of tags is greater than 5
        if self.tags.count() > 5:
            raise ValidationError('A recipe can have at most 5 tags.')

    def __str__(self):
        return self.title
