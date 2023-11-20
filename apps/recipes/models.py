from django.db import models
from django.utils.translation import gettext_lazy as _

from core import settings


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
    preparation_time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    difficulty_level = models.PositiveSmallIntegerField(
        choices=DIFFICULTY_CHOICES,
        default=0,  # Start with 0 (Not chosen)
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def get_competence_level_display(self):
        for level, label in self.DIFFICULTY_CHOICES:
            if level == self.difficulty_level:
                return label
        return None  # Return None if no match is found

    def __str__(self):
        return self.title
