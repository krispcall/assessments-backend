from accounts.apis.v1.throttling import CustomRateThrottle
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from books.models import Book
from rest_framework_simplejwt.authentication import JWTAuthentication
from books.apis.v1.serializers import BookSerializer
from drf_yasg.utils import swagger_auto_schema



class BookViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing and retrieving books.
    Applies subscription-based throttling:
        - FREE: 100/day
        - BASIC: 1000/day
        - PRO: unlimited
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [CustomRateThrottle]


    @swagger_auto_schema(
        operation_summary="list of the books",
        operation_description="list of the books",
        request_body=None,
        tags=["Books Endpoints"],
        security=[{'Bearer': []}]
    )
    def list(self, request):
        """
        GET /books/
        Retrieve a list of books.
        """
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Retrive books",
        operation_description="books",
        request_body=None,
        tags=["Books Endpoints"],
        security=[{'Bearer': []}]
    )
    def retrieve(self, request, pk=None):
        """
        GET /books/{id}/
        Retrieve a single book by ID.
        """
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)