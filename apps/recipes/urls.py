from django.urls import path

from apps.recipes.views import GetAllRecipes

app_name = 'recipes'

urlpatterns = [
    path('all/', GetAllRecipes.as_view(), name='recipe-list'),
]