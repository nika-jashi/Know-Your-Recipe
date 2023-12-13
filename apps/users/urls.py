from django.urls import path

from apps.ingredients.views import GetAllIngredientsView
from apps.recipes.views import MyRecipesView
from apps.tags.views import MyTagsView
from apps.users.views import (
    UserRegistrationView,
    AccountLoginView,
    AccountProfileView,
    UserChangePasswordView
)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('profile/', AccountProfileView.as_view(), name='profile'),
    path('change/password/', UserChangePasswordView.as_view(), name='password-change'),
    path('my-recipes/', MyRecipesView.as_view(), name='my-recipes'),
    path('my-tags/', MyTagsView.as_view(), name='my-tags'),
    path('my-ingredients/', GetAllIngredientsView.as_view(), name='ingredient-list'),
]
