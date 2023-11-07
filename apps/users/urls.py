from django.urls import path
from apps.users.views import (
    UserRegistrationView, AccountLoginView
)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', AccountLoginView.as_view(), name='login'),
]
