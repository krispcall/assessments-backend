import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/assignment_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
    CHUNK_DIR = os.path.join(UPLOAD_DIR, 'chunks')
    FINAL_DIR = os.path.join(UPLOAD_DIR, 'final')
    ALLOWED_EXTENSTION = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0