"""
URL configuration for email_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger / Redoc schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Email Validation API",
        default_version='v1',
        description="API to validate emails (format, DNS, SPF, DKIM, DMARC, SMTP)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # allow any user to access
    permission_classes=(permissions.AllowAny,),  # no authentication required
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Your app URLs
    path('api/', include('file.urls')),  # keeps your existing app routes

    # Swagger JSON / YAML schema
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Swagger UI (interactive documentation)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc UI (clean documentation)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
