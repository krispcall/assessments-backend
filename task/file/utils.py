# chunked_upload/utils.py
import os
import hashlib
from django.conf import settings
from cryptography.fernet import Fernet, InvalidToken

from django.core.files.base import File

CHUNKS_TEMP_DIR = os.path.join(settings.MEDIA_ROOT, 'temp_chunks')

def compute_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def assemble_chunks_to_file(upload_session, destination_path):
    """
    Reassemble chunk files into destination path.
    chunk files stored in CHUNKS_TEMP_DIR/<upload_id>/<index>.part
    """
    upload_dir = os.path.join(CHUNKS_TEMP_DIR, str(upload_session.upload_id))
    if not os.path.exists(upload_dir):
        raise FileNotFoundError("No chunks directory.")

    # gather chunk files sorted by index
    files = []
    for cm in upload_session.chunks.all().order_by('chunk_index'):
        files.append(cm.path)

    # Write to destination file
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(destination_path, 'wb') as dest:
        for p in files:
            with open(p, 'rb') as src:
                for data in iter(lambda: src.read(1048576), b''):
                    dest.write(data)
    return destination_path

# Encryption helper using Fernet (symmetric)
def get_fernet():
    key = getattr(settings, 'FILE_ENCRYPTION_KEY', None)
    if not key:
        raise RuntimeError("FILE_ENCRYPTION_KEY not set in settings.")
    return Fernet(key)

def encrypt_file_inplace(path):
    f = get_fernet()
    with open(path, 'rb') as fo:
        data = fo.read()
    token = f.encrypt(data)
    with open(path, 'wb') as fo:
        fo.write(token)
    return path

def decrypt_bytes(data_bytes):
    f = get_fernet()
    return f.decrypt(data_bytes)
