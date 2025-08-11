from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static



admin.site.site_header = "Book Management System"
admin.site.site_title = "Book Management System Admin Portal"
admin.site.index_title = "Welcome to Book Management System Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]