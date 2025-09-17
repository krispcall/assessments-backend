from django.contrib import admin
from .models import ChunkMeta,UploadSession,UploadQuota
# Register your models here.


admin.site.register([ChunkMeta,UploadQuota,UploadSession])