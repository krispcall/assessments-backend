# README

**Technical Assessment Backend Engineer**

All the assessments and further instructions will be provided via Issues.

### NOTE
1. Please submit the working code.
2. Please do not share the solutions with anyone else.
3. Copyrights of the submitted solution will be the of the company.
# Chunked File Upload Service

This project is a Django + Django REST Framework application that supports large file uploads by splitting them into smaller chunks. It uses Celery with Redis for asynchronous background processing and enforces per-user quotas.

## Features

* Upload large files in chunks
* Track upload progress with `UploadSession`
* User upload quota enforcement (daily and monthly)
* File type validation (CSV files allowed by default)
* Asynchronous file assembly with Celery
* API documentation with Swagger (drf-yasg)

## Requirements

* Python 3.12+
* Django 5.x
* Django REST Framework
* Celery
* Redis
* drf-yasg
* python-dotenv

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/chunked-upload.git
   cd chunked-upload
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/1
   ```

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

## Running the Project

Start Django:

```bash
python manage.py runserver
```

Start Celery worker:

```bash
celery -A task worker -l info
```

## Running with Docker

You can also run the project using Docker Compose:

```bash
docker-compose up --build
```

## API Endpoints

* `POST /upload-sessions/` - Create upload session
* `POST /upload-chunk/` - Upload chunk
* `POST /finalize-upload/` - Finalize and trigger assembly
* `GET /upload-status/{upload_id}/` - Check status
* `GET /chunks/{upload_id}/` - List received chunks

Swagger documentation is available at:

```
http://localhost:8000/swagger/
```

## Notes

* Uploaded chunks are stored temporarily in `MEDIA_ROOT/temp_chunks/`
* Assembled files are stored in `MEDIA_ROOT/uploads/`
* Default quotas: 10 GB per day and 100 GB per month per user
