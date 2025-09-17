from django.db import models
import os
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

STATUS_CHOICES = [
    ('uploading', 'Uploading'),
    ('uploaded', 'Uploaded'),
    ('assembling', 'Assembling'),
    ('processing', 'Processing'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('cancelled', 'Cancelled'),
]

def temp_chunk_path(instance, filename):
    # store under MEDIA_ROOT/chunks/<upload_id>/<chunk_index>
    return f"chunks/{instance.upload_session.upload_id}/{instance.chunk_index}.part"

class UploadSession(models.Model):
    upload_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads',null=True,blank=True)
    filename = models.CharField(max_length=512)
    total_size = models.BigIntegerField(null=True, blank=True)  # bytes
    total_chunks = models.IntegerField(null=True, blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    checksum = models.CharField(max_length=128, blank=True)  # e.g., sha256 from client (optional)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    received_bytes = models.BigIntegerField(default=0)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='uploading')
    error = models.TextField(blank=True)

    # after assembled:
    assembled_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return f"{self.upload_id} - {self.filename} - {self.status}"

class ChunkMeta(models.Model):
    upload_session = models.ForeignKey(UploadSession, on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.IntegerField()
    size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=1024)  # path in storage
    received = models.BooleanField(default=True)

    class Meta:
        unique_together = ('upload_session', 'chunk_index')

    def __str__(self):
        return f"{self.upload_session.upload_id} chunk {self.chunk_index}"

class UploadQuota(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='upload_quota')
    daily_bytes = models.BigIntegerField(default=10 * 1024**3)  # 10 GB default per day
    monthly_bytes = models.BigIntegerField(default=100 * 1024**3)  # 100 GB default per month
    used_daily = models.BigIntegerField(default=0)
    used_monthly = models.BigIntegerField(default=0)
    last_reset = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Quota({self.owner})"

