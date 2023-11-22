from django.urls import path

from apps.tags.views import (
    CreateTagView,
    GetAllRecipesView
)

app_name = 'tags'

urlpatterns = [
    path('all/', GetAllRecipesView.as_view(), name='tag-list'),
    path('create/', CreateTagView.as_view(), name='tag-create'),
]
