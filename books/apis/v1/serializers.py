from rest_framework import serializers
from books.models import Book, Upload, UploadChunk

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
        fields = ['id', 'title', 'content', 'author', 'publish_date']

class UploadSerializer(serializers.ModelSerializer):
    """
    Serializer representing an upload model.
    Base classes:
        - serializers.ModelSerializer
    Returns:
        - UploadSerializer: A serializer instance for upload fields.
    """
    class Meta:
        model = Upload
        fields = ['upload_id', 'filename', 'total_size', 'content_type', 'status', 'chunks_received', 'total_chunks']

class UploadChunkSerializer(serializers.ModelSerializer):
    """
    Serializer representing an upload chunk model.
    Base classes:
        - serializers.ModelSerializer
    Returns:
        - UploadChunkSerializer: A serializer instance for upload chunk fields.
    """
    upload = serializers.UUIDField()
    chunk_file = serializers.FileField()
    chunk_hash = serializers.CharField()
    class Meta:
        model = UploadChunk
        fields = ['upload', 'chunk_number', 'chunk_file', 'chunk_hash']


class UploadStatusSerializer(serializers.ModelSerializer):
    """
    Serializer representing an upload model with progress information.
    Base classes:
        - serializers.ModelSerializer
    Returns:
        - UploadStatusSerializer: A serializer instance for upload status fields.
    """
    progress = serializers.SerializerMethodField()

    def get_progress(self, obj):
        """
        Calculate the upload progress as a percentage.
        Args:
            - obj: Upload instance
        Returns:
            - float: Progress percentage (0-100)
        """
        return (obj.chunks_received / obj.total_chunks * 100) if obj.total_chunks > 0 else 0

    class Meta:
        model = Upload
        fields = ['upload_id', 'status', 'progress', 'error_message']