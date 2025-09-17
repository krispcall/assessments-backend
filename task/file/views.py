# chunked_upload/views.py
import os
import hashlib
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import UploadSession, ChunkMeta, UploadQuota
from .serializer import UploadSessionCreateSerializer, UploadSessionStatusSerializer,UploadChunkSerializer,FinalizeUploadSerializer
from .tasks import assemble_file_task  # Celery task we'll define
from django.core.files.base import ContentFile
from django.db import transaction
from datetime import date
from django.db.models import Sum
from rest_framework.exceptions import ValidationError



CHUNKS_TEMP_DIR = os.path.join(settings.MEDIA_ROOT, 'temp_chunks')  # ensure exists

class UploadSessionCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UploadSessionCreateSerializer

    def perform_create(self, serializer):
        content_type = self.request.data.get("content_type", "")
        if content_type not in ("text/csv", "application/vnd.ms-excel"):
            raise ValidationError({"detail": "Invalid file type. Only CSVs are allowed."})

        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(owner=user)


class UploadChunkView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UploadChunkSerializer

    def post(self, request, format=None):
        # Use serializer to parse input
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        upload_id = serializer.validated_data['upload_id']
        chunk_index = serializer.validated_data['chunk_index']
        chunk_data = serializer.validated_data.get('file') or request.body

        # Fetch upload session
        session = get_object_or_404(UploadSession, upload_id=upload_id, owner=request.user)

        if session.status != 'uploading':
            return Response({'detail': f'Upload session status is {session.status}, cannot accept chunks.'}, status=400)

        # Enforce quotas
        if not self._check_quota(request.user, len(chunk_data)):
            return Response({'detail': 'Upload quota exceeded.'}, status=403)

        # Save chunk to disk
        upload_dir = os.path.join(CHUNKS_TEMP_DIR, str(session.upload_id))
        os.makedirs(upload_dir, exist_ok=True)
        chunk_filename = os.path.join(upload_dir, f"{chunk_index}.part")

        with open(chunk_filename, 'wb') as f:
            if hasattr(chunk_data, 'read'):
                for chunk in chunk_data.chunks():
                    f.write(chunk)
                size = f.tell()
            else:
                f.write(chunk_data)
                size = len(chunk_data)

        # Persist chunk metadata
        cm, created = ChunkMeta.objects.update_or_create(
            upload_session=session, chunk_index=chunk_index,
            defaults={'size': size, 'path': chunk_filename, 'received': True}
        )

        # Update received_bytes
        total_received = session.chunks.aggregate(total=Sum('size'))['total'] or 0
        session.received_bytes = total_received
        session.save(update_fields=['received_bytes', 'updated_at'])

        # Trigger assembly if all chunks received
        if session.total_chunks and session.chunks.count() >= session.total_chunks:
            session.status = 'uploaded'
            session.save(update_fields=['status'])
            assemble_file_task.delay(str(session.upload_id), request.user.pk)

        return Response({'detail': 'Chunk received', 'chunk_index': chunk_index}, status=201)

    def _check_quota(self, user, incoming_bytes):
        quota, _ = UploadQuota.objects.get_or_create(owner=user)
        today = date.today()
        if quota.last_reset != today:
            quota.used_daily = 0
            quota.last_reset = today
        if quota.used_daily + incoming_bytes > quota.daily_bytes:
            return False
        quota.used_daily += incoming_bytes
        quota.used_monthly += incoming_bytes
        quota.save(update_fields=['used_daily', 'used_monthly', 'last_reset'])
        return True


class FinalizeUploadView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FinalizeUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        upload_id = serializer.validated_data['upload_id']
        total_chunks = serializer.validated_data.get('total_chunks')

        # Fetch the upload session
        session = get_object_or_404(UploadSession, upload_id=upload_id, owner=request.user)

        # Update total_chunks if provided
        if total_chunks:
            session.total_chunks = total_chunks
            session.save(update_fields=['total_chunks'])

        # Check if all chunks received
        if session.total_chunks and session.chunks.count() >= session.total_chunks:
            session.status = 'uploaded'
            session.save(update_fields=['status'])
            assemble_file_task.delay(str(session.upload_id), request.user.pk)
            return Response({'detail': 'Finalize triggered; assembly queued.'})
        else:
            return Response({'detail': 'Not all chunks received yet.'}, status=status.HTTP_400_BAD_REQUEST)
        

class UploadStatusView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UploadSessionStatusSerializer
    lookup_field = 'upload_id'
    queryset = UploadSession.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied()
        return obj

class ChunkListView(ListAPIView):
    permission_classes = (AllowAny,)
    def get(self, request, upload_id):
        session = get_object_or_404(UploadSession, upload_id=upload_id, owner=request.user)
        indices = list(session.chunks.values_list('chunk_index', flat=True))
        return Response({'received_chunks': indices})
