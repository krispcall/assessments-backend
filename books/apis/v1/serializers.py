from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer representing a books model.
    Base classes:
        - serializers.ModelSerializer
    Returns:
        - BookSerializer: A serializer instance for books fields.
    """
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'file']