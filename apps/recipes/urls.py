from django.urls import path

from apps.recipes.views import (
    GetAllRecipesView,
    DetailedRecipeView,
    CreateRecipeView
)

app_name = 'recipes'

urlpatterns = [
    path('all/', GetAllRecipesView.as_view(), name='recipe-list'),
    path('item/<int:pk>/', DetailedRecipeView.as_view(), name='recipe-detail'),
    path('create/', CreateRecipeView.as_view(), name='recipe-create'),
]
