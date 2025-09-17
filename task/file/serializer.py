from rest_framework import serializers
from .models import UploadSession, ChunkMeta

class UploadSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadSession
        fields = ('upload_id', 'filename', 'total_size', 'total_chunks', 'content_type', 'checksum')
        read_only_fields = ('upload_id',)

class UploadSessionStatusSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    class Meta:
        model = UploadSession
        fields = ('upload_id', 'filename', 'total_size', 'received_bytes', 'status', 'progress', 'total_chunks', 'checksum', 'error', 'created_at', 'updated_at')

    def get_progress(self, obj):
        if not obj.total_size:
            return None
        try:
            return round((obj.received_bytes / obj.total_size) * 100, 2)
        except Exception:
            return None


class UploadChunkSerializer(serializers.Serializer):
    upload_id = serializers.UUIDField()
    chunk_index = serializers.IntegerField()
    file = serializers.FileField()  # optional if raw body is used



class FinalizeUploadSerializer(serializers.Serializer):
    upload_id = serializers.UUIDField()
    total_chunks = serializers.IntegerField(required=False, min_value=1)