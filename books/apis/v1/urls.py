from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UploadViewSet

router = DefaultRouter()
router.register(r'uploads', UploadViewSet, basename='upload')
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]