from django.urls import path
from .views import UploadSessionCreateView, UploadChunkView, FinalizeUploadView, UploadStatusView, ChunkListView

urlpatterns = [
    path('sessions/', UploadSessionCreateView.as_view(), name='create_session'),
    path('chunk/', UploadChunkView.as_view(), name='upload_chunk'),
    path('finalize/', FinalizeUploadView.as_view(), name='finalize_upload'),
    path('status/<uuid:upload_id>/', UploadStatusView.as_view(), name='upload_status'),
    path('chunks/<uuid:upload_id>/', ChunkListView.as_view(), name='chunk_list'),
]
