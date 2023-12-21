from django.conf.urls.static import static
from django.urls import path

from apps.recipes.views import (
    GetAllRecipesView,
    DetailedRecipeView,
    CreateRecipeView,
    SaveRecipeView,
)
from core import settings

app_name = 'recipes'

urlpatterns = [
    path('all/', GetAllRecipesView.as_view(), name='recipe-list'),
    path('item/<int:pk>/', DetailedRecipeView.as_view(), name='recipe-detail'),
    path('create/', CreateRecipeView.as_view(), name='recipe-create'),
    path('item/download/<int:pk>/', SaveRecipeView.as_view(), name='recipe-download'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
