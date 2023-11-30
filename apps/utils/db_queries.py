from apps.recipes.serializers import RecipeSerializer
from apps.tags.models import Tag
from apps.tags.serializers import TagSerializer
from apps.users.models import CustomUser
from apps.recipes.models import Recipe


def check_user_exists(uid=None, email=None, username=None) -> bool:
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
    recipes = Recipe.objects.all().order_by('-created_at')
    recipes_data = RecipeSerializer(instance=recipes, many=True)
    return recipes_data


def get_all_tags():
    tags = Tag.objects.all().order_by('-created_at')
    tags_data = TagSerializer(instance=tags, many=True)
    return tags_data


def get_recipe_by_id(pk: int) -> Recipe:
    recipe = Recipe.objects.filter(pk=pk).first()
    return recipe


def get_tag_by_id(pk: int) -> Tag:
    tag = Tag.objects.filter(pk=pk).first()
    return tag


def get_recipe_owner(request, recipe_pk) -> bool:
    recipe = Recipe.objects.filter(pk=recipe_pk).first()
    if recipe.user != request.user:
        return False
    return True


def get_tag_owner(request, tag_pk) -> bool:
    tag = Tag.objects.filter(pk=tag_pk).first()
    if tag.creator != request.user:
        return False
    return True


def get_my_recipes(request) -> RecipeSerializer:
    my_recipes = Recipe.objects.filter(user=request.user).order_by('-created_at')
    recipes_data = RecipeSerializer(instance=my_recipes, many=True)
    return recipes_data


def get_my_tags(request) -> TagSerializer:
    my_tags = Tag.objects.filter(creator=request.user).order_by('-created_at')
    tags_data = TagSerializer(instance=my_tags, many=True)
    return tags_data
