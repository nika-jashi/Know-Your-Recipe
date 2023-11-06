from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # urls for SWAGGER UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('user/', include('apps.users.urls')),
]
