from django.urls import path

from apps.tags.views import (
    CreateTagView,
    GetAllTagsView,
    DetailedTagView
)

app_name = 'tags'

urlpatterns = [
    path('all/', GetAllTagsView.as_view(), name='tag-list'),
    path('item/<int:pk>/', DetailedTagView.as_view(), name='tag-detail'),
    path('create/', CreateTagView.as_view(), name='tag-create'),
]
