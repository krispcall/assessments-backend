# chunked_upload/tasks.py
import os
from celery import shared_task
from django.conf import settings
from .models import UploadSession
from .utils import assemble_chunks_to_file, compute_sha256, encrypt_file_inplace
from django.core.files import File
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def assemble_file_task(self, upload_id, user_pk):
    try:
        session = UploadSession.objects.get(upload_id=upload_id)
        session.status = 'assembling'
        session.save(update_fields=['status'])
        dest_dir = os.path.join(settings.MEDIA_ROOT, 'assembled')
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, f"{upload_id}_{session.filename}")

        assemble_chunks_to_file(session, dest_path)

        # verify checksum if provided
        computed = compute_sha256(dest_path)
        if session.checksum:
            if computed.lower() != session.checksum.lower():
                session.status = 'failed'
                session.error = f"Checksum mismatch: expected {session.checksum}, got {computed}"
                session.save(update_fields=['status', 'error'])
                return

        # encrypt at rest if enabled
        if getattr(settings, 'ENCRYPT_UPLOADS_AT_REST', False):
            encrypt_file_inplace(dest_path)

        # save assembled file to FileField (this moves file into Django storage)
        with open(dest_path, 'rb') as f:
            django_file = File(f)
            session.assembled_file.save(os.path.basename(dest_path), django_file, save=True)

        session.status = 'processing'
        session.save(update_fields=['status'])

        # enqueue processing task (implement process_file_task)
        process_file_task.delay(str(session.upload_id))
    except Exception as exc:
        logger.exception("Error assembling upload %s", upload_id)
        try:
            session.status = 'failed'
            session.error = str(exc)
            session.save(update_fields=['status', 'error'])
        except:
            pass
        raise

@shared_task
def process_file_task(upload_id):
    # Example CSV parser: parse session.assembled_file and insert rows.
    from .models import UploadSession
    session = UploadSession.objects.get(upload_id=upload_id)
    # Mark processing start
    session.status = 'processing'
    session.save(update_fields=['status'])
    try:
        # If encrypted at rest, decrypt bytes first (skip in this example)
        # For demonstration: if content-type is CSV, stream parse
        if session.assembled_file:
            path = session.assembled_file.path
            # if encrypted, decrypt on the fly or use a streaming decrypt approach (not implemented)
            # simple CSV processing (line count)
            count = 0
            import csv
            with open(path, 'rb') as f:
                # If encrypted, decrypt bytes then process.
                if getattr(settings, 'ENCRYPT_UPLOADS_AT_REST', False):
                    from .utils import get_fernet
                    fernet = get_fernet()
                    raw = f.read()
                    data = fernet.decrypt(raw)
                    text = data.decode('utf-8', errors='ignore').splitlines()
                    reader = csv.reader(text)
                    for _ in reader:
                        count += 1
                else:
                    # assume utf-8 text
                    for line in f:
                        count += 1
            # After processing
            session.status = 'completed'
            session.save(update_fields=['status'])
            # Optionally store result summary in session.meta or another model
        else:
            session.status = 'failed'
            session.error = "No assembled file to process."
            session.save(update_fields=['status','error'])
    except Exception as exc:
        session.status = 'failed'
        session.error = str(exc)
        session.save(update_fields=['status','error'])
        raise
