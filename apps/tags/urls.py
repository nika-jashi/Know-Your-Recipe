from django.urls import path

from apps.tags.views import (
    CreateTagView,
    GetAllRecipesView,
    DetailedTagView
)

app_name = 'tags'

urlpatterns = [
    path('all/', GetAllRecipesView.as_view(), name='tag-list'),
    path('item/<int:pk>/', DetailedTagView.as_view(), name='tag-detail'),
    path('create/', CreateTagView.as_view(), name='tag-create'),
]
