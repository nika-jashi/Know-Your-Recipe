from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.ingredients.models import Ingredient
from apps.ingredients.serializers import IngredientSerializer


class IngredientViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Manage ingredients in the database."""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
