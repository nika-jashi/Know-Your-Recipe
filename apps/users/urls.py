from django.urls import path

from apps.recipes.views import MyRecipesView
from apps.tags.views import MyTagsView
from apps.users.views import (
    UserRegistrationView,
    AccountLoginView,
    AccountProfileView,
    UserChangePasswordView, PasswordResetRequestEmailView, PasswordResetVerifyEmailView, PasswordResetConfirmView
)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('profile/', AccountProfileView.as_view(), name='profile'),
    path('change/password/', UserChangePasswordView.as_view(), name='password-change'),
    path('my-recipes/', MyRecipesView.as_view(), name='my-recipes'),
    path('my-tags/', MyTagsView.as_view(), name='my-tags'),

    path('reset-password/', PasswordResetRequestEmailView.as_view(), name='reset-password'),
    path('reset-password/verify/', PasswordResetVerifyEmailView.as_view(), name='reset-password-verify'),
    path('reset-password/confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
]
