from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

schema_view = get_schema_view(
    openapi.Info(
       title="Library API",
       default_version='v1',
       description="Library API endpoints",
       terms_of_service="https://www.example.com/policies/terms/",
       contact=openapi.Contact(email="contact@example.com"),
       license=openapi.License(name="BSD License"),
    ),
    patterns=[
        path("api/base/", include("base.urls")),
    ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path("doc/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('admin/', admin.site.urls),
    path("api/base/", include("base.urls")),
]

