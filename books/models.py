import uuid, os
from django.db import models
from accounts.models import User


class Book(models.Model):
    """
    Book model to store books details.
    Base classes:
        - Model
    Returns:
        None
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    content = models.TextField()
    publish_date = models.CharField(max_length=2555)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'book'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class Upload(models.Model):
    """
    Model to track file upload sessions for large files (e.g., CSVs up to 5GB).
    """
    upload_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    filename = models.CharField(max_length=255)
    total_size = models.BigIntegerField()
    content_type = models.CharField(max_length=100, default='text/csv')
    status = models.CharField(
        max_length=20,
        choices=[
            ('initialized', 'Initialized'),
            ('uploading', 'Uploading'),
            ('uploaded', 'Uploaded'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('error', 'Error')
        ],
        default='initialized'
    )
    chunks_received = models.PositiveIntegerField(default=0)
    total_chunks = models.PositiveIntegerField()
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Upload {self.upload_id} ({self.filename})"

    class Meta:
        db_table = 'upload'
        verbose_name = 'Upload'
        verbose_name_plural = 'Uploads'

class UploadChunk(models.Model):
    """
    Model to store individual chunks of an upload.
    """
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, related_name='chunks')
    chunk_number = models.PositiveIntegerField()
    chunk_file = models.FileField(upload_to='chunks/%Y/%m/%d/')
    chunk_hash = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'upload_chunk'
        unique_together = ('upload', 'chunk_number')
        verbose_name = 'Upload Chunk'
        verbose_name_plural = 'Upload Chunks'
    
    def delete(self, *args, **kwargs):
        if self.chunk_file and os.path.isfile(self.chunk_file.path):
            os.remove(self.chunk_file.path)
        super().delete(*args, **kwargs)