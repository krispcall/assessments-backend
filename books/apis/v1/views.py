from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from books.models import Upload, UploadChunk, Book
from books.apis.v1.serializers import UploadSerializer, UploadStatusSerializer, BookSerializer, UploadChunkSerializer
from accounts.apis.v1.throttling import CustomRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
import hashlib
import os, math
from django.conf import settings
from celery import shared_task
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_datetime

class BookViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing and retrieving books.
    Applies subscription-based throttling:
        - FREE: 100/day
        - BASIC: 1000/day
        - PRO: unlimited
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomRateThrottle]

    def get_queryset(self):
        """
        Get the queryset filtered by the authenticated user.
        """
        return Book.objects.filter(uploads__user=self.request.user).distinct()

    @swagger_auto_schema(
        operation_summary="List books",
        operation_description="Retrieves a list of books for the authenticated user.",
        request_body=None,
        tags=["Books Endpoints"],
        security=[{'Bearer': []}],
        responses={
            200: BookSerializer(many=True),
            401: "Unauthorized"
        }
    )
    def list(self, request):
        """
        GET /books/
        Retrieve a list of books.
        """
        queryset = self.get_queryset()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Retrieve a book",
        operation_description="Retrieves a single book by ID.",
        request_body=None,
        tags=["Books Endpoints"],
        security=[{'Bearer': []}],
        responses={
            200: BookSerializer,
            404: "Book not found",
            401: "Unauthorized"
        }
    )
    def retrieve(self, request, pk=None):
        """
        GET /books/{id}/
        Retrieve a single book by ID.
        """
        try:
            book = Book.objects.get(pk=pk, uploads__user=self.request.user)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UploadViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling chunked file uploads and processing.
    Applies subscription-based throttling:
        - FREE: 100/day
        - BASIC: 1000/day
        - PRO: unlimited
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomRateThrottle]

    def get_queryset(self):
        """
        Get the queryset filtered by the authenticated user.
        """
        return Upload.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Initialize a new upload session",
        operation_description="Creates a new upload session for a CSV file and returns the upload ID and chunk size.",
        request_body=UploadSerializer,
        tags=["Bulk csv Books Endpoints"],
        security=[{'Bearer': []}],
        responses={
            201: "Upload session created with upload_id and chunk_size",
            400: "Invalid input data"
        }
    )
    @action(detail=False, methods=['post'])
    def init(self, request):
        """
        POST /uploads/init/
        Initialize a new upload session.
        """
        serializer = UploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        filename = serializer.validated_data['filename']
        total_size = serializer.validated_data['total_size']
        content_type = serializer.validated_data.get('content_type', 'text/csv')

        chunk_size = 50 * 1024 * 1024
        total_chunks = math.floor((total_size + chunk_size - 1) // chunk_size) + 1
        print("********",total_chunks, "********************************************")

        upload = Upload.objects.create(
            user=self.request.user,
            filename=filename,
            total_size=total_size,
            content_type=content_type,
            total_chunks=total_chunks
        )
        return Response({
            'upload_id': str(upload.upload_id),
            'chunk_size': chunk_size
        }, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Upload a file chunk",
        operation_description="Uploads a chunk of the CSV file for a given upload session.",
        request_body=UploadChunkSerializer,
        tags=["Bulk csv Books Endpoints"],
        security=[{'Bearer': []}],
        responses={
            200: "Chunk received",
            400: "Invalid chunk data",
            404: "Upload not found"
        }
    )
    @action(detail=True, methods=['post'])
    def chunk(self, request, pk=None):
        """
        POST /uploads/{upload_id}/chunk/
        Upload a chunk of the file.
        """
        try:
            upload = self.get_queryset().get(upload_id=pk)
        except ObjectDoesNotExist:
            return Response({"detail": "Upload not found."}, status=status.HTTP_404_NOT_FOUND)

        chunk_number = request.data.get('chunk_number')
        chunk_file = request.FILES.get('chunk')
        chunk_hash = request.data.get('chunk_hash')

        if not all([chunk_number is not None, chunk_file, chunk_hash]):
            return Response({"detail": "Missing chunk data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            chunk_number = int(chunk_number)
        except (TypeError, ValueError):
            return Response({"detail": "Invalid chunk_number."}, status=status.HTTP_400_BAD_REQUEST)

        computed_hash = hashlib.md5(chunk_file.read()).hexdigest()
        chunk_file.seek(0)
        if computed_hash != chunk_hash:
            return Response({"detail": "Hash mismatch."}, status=status.HTTP_400_BAD_REQUEST)

        UploadChunk.objects.create(
            upload=upload,
            chunk_number=chunk_number,
            chunk_file=chunk_file,
            chunk_hash=chunk_hash
        )
        upload.chunks_received += 1
        upload.status = 'uploading'
        upload.save()
        return Response({"status": "chunk_received"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Complete an upload session",
        operation_description="Completes the upload session and enqueues the file for processing.",
        request_body=None,
        tags=["Bulk csv Books Endpoints"],
        security=[{'Bearer': []}],
        responses={
            200: "Upload completed",
            400: "Invalid total_chunks",
            404: "Upload not found"
        }
    )
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        POST /uploads/{upload_id}/complete/
        Complete the upload and enqueue processing.
        """
        try:
            upload = self.get_queryset().get(upload_id=pk)
        except ObjectDoesNotExist:
            return Response({"detail": "Upload not found."}, status=status.HTTP_404_NOT_FOUND)

        total_chunks = request.data.get('total_chunks')
        if not total_chunks:
            return Response({"detail": "Missing total_chunks."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            total_chunks = int(total_chunks)
        except (TypeError, ValueError):
            return Response({"detail": "Invalid total_chunks."}, status=status.HTTP_400_BAD_REQUEST)
        print(upload.chunks_received, total_chunks, upload.total_chunks, '**********************************')
        if upload.chunks_received != total_chunks or upload.total_chunks != total_chunks:
            return Response({"detail": "Incomplete chunks."}, status=status.HTTP_400_BAD_REQUEST)

        file_path = assemble_file(upload)
        upload.status = 'uploaded'
        upload.save()
        process_file_task.delay(str(upload.upload_id), file_path)
        return Response({
            "status": "upload_complete",
            "file_id": str(upload.upload_id)
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Retrieve upload status",
        operation_description="Retrieves the status and progress of an upload session.",
        request_body=None,
        tags=["Bulk csv Books Endpoints"],
        security=[{'Bearer': []}],
        responses={
            200: UploadStatusSerializer,
            404: "Upload not found"
        }
    )
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        GET /uploads/{upload_id}/status/
        Retrieve the status of an upload.
        """
        try:
            upload = self.get_queryset().get(upload_id=pk)
        except ObjectDoesNotExist:
            return Response({"detail": "Upload not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UploadStatusSerializer(upload)
        return Response(serializer.data, status=status.HTTP_200_OK)

def assemble_file(upload):
    """
    Assemble uploaded chunks into a single file.
    """
    output_path = os.path.join(settings.MEDIA_ROOT, 'uploads', str(upload.upload_id), upload.filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as output_file:
        for chunk in upload.chunks.order_by('chunk_number'):
            with chunk.chunk_file.open('rb') as chunk_file:
                output_file.write(chunk_file.read())
    return output_path

@shared_task
def process_file_task(upload_id, file_path):
    """
    Process the uploaded CSV file to create Book instances without linking to Upload.
    """
    try:
        # Mark upload status as processing (optional)
        upload = Upload.objects.get(upload_id=upload_id)
        upload.status = 'processing'
        upload.save()

        required_columns = ['title', 'content', 'author', 'publish_date']
        for chunk in pd.read_csv(file_path, chunksize=10000):
            if not all(col in chunk.columns for col in required_columns):
                raise ValueError("CSV missing required columns: title, content, author, publish_date")

            books_to_create = []
            for _, row in chunk.iterrows():
                books_to_create.append(Book(
                    title=str(row['title']).strip()[:255],
                    content=str(row.get('content', '')).strip(),
                    author=str(row['author']).strip()[:255],
                    publish_date=str(row['publish_date']).strip(),
                ))

            # Bulk create books without linking to upload
            Book.objects.bulk_create(books_to_create)

        upload.status = 'completed'
        upload.save()

        # Cleanup temporary chunks
        for chunk in upload.chunks.all():
            chunk.chunk_file.delete()
            chunk.delete()
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        upload.status = 'error'
        upload.error_message = str(e)
        upload.save()
        raise

