from typing import List

from apps.recipes.serializers import RecipeSerializer
from apps.users.models import CustomUser
from apps.recipes.models import Recipe


def check_user_exists(uid=None, email=None, username=None):
    return (
        CustomUser.objects.filter(id=uid).exists() if uid is not None else
        CustomUser.objects.filter(email=email).exists() if email is not None else
        CustomUser.objects.filter(username=username).exists() if username is not None else
        False
    )


def get_user(uid: int = None, email: str = None, username: str = None) -> CustomUser:
    user_object = (
            CustomUser.objects.filter(id=uid).first() or
            CustomUser.objects.filter(email=email).first() or
            CustomUser.objects.filter(username=username).first() or
            None
    )
    return user_object


def get_all_recipes():
    recipes = Recipe.objects.all().order_by('-id')
    recipe_data = RecipeSerializer(recipes, many=True).data
    return recipe_data

