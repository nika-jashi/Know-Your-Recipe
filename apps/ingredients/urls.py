from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.ingredients.views import IngredientViewSet

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)

app_name = 'ingredients'

urlpatterns = [
    path('', include(router.urls)),
]
