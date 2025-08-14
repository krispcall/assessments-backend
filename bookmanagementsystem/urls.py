from drf_yasg import openapi
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from accounts import views as acc_views
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static



admin.site.site_header = "Book Management System"
admin.site.site_title = "Book Management System Admin Portal"
admin.site.index_title = "Welcome to Book Management System Admin Portal"


schema_view = get_schema_view(
    openapi.Info(
        title="Book Management System API",
        default_version="v1",
        description=(
            "this is the apis list"
        ),
        terms_of_service="https://www.homprasaddhakal.com.np",
        contact=openapi.Contact(email="homprasaddhakal@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', acc_views.landing_page, name="homepage"),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('accounts.apis.v1.urls')),
    path('', include('books.apis.v1.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]