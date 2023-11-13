from django.urls import path

from apps.recipes.views import GetAllRecipesView, DetailedRecipeView

app_name = 'recipes'

urlpatterns = [
    path('all/', GetAllRecipesView.as_view(), name='recipe-list'),
    path('recipe-detail/<int:pk>/', DetailedRecipeView.as_view(), name='recipe-detail'),
]
