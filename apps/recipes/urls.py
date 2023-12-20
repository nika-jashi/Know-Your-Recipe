from django.conf.urls.static import static
from django.urls import path

from apps.recipes.views import (
    GetAllRecipesView,
    DetailedRecipeView,
    CreateRecipeView,
    UploadRecipeImageView,
)
from core import settings

app_name = 'recipes'

urlpatterns = [
    path('all/', GetAllRecipesView.as_view(), name='recipe-list'),
    path('item/<int:pk>/', DetailedRecipeView.as_view(), name='recipe-detail'),
    path('create/', CreateRecipeView.as_view(), name='recipe-create'),
    path('item/<int:pk>/upload-image/', UploadRecipeImageView.as_view(), name='recipe-upload-image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
