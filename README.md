# Task1 API – Rate Limiting & Abuse Detection

This project is a Django REST Framework (DRF) API that provides rate limiting, abuse detection, and subscription-based API access. Users can be blocked temporarily if suspicious activity is detected. The project also includes Swagger documentation for all endpoints.

## Features

- API Key authentication for all requests
- Subscription plans with daily request limits:
  - Free: 100 requests/day
  - Basic: 1,000 requests/day
  - Pro: Unlimited
- Rate limiting per user and IP address
- Abuse detection for rapid API key switching and high-frequency requests
- Logging of all requests and limit breaches
- Admin APIs to view and unblock blocked users/IPs
- Swagger documentation at `/swagger/` and `/redoc/`
- PostgreSQL database
- Optional Redis for caching
- Dockerized setup for easy deployment

## Project Structure

task1/
│── api/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│ ├── middleware.py
│ └── utils/
│ └── rate_limiter.py
│
│── task1/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
│── Dockerfile
│── docker-compose.yml
│── requirements.txt
│── .env.example
└── README.md

bash
Copy code

Installation

Clone the repository
git clone https://github.com/your-username/task1-api.git
cd task1-api

Create a virtual environment
For Linux/macOS: python3 -m venv venv and source venv/bin/activate
For Windows: python3 -m venv venv and venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Configure environment variables
Copy .env.example to .env and update the database credentials and other settings.

Run database migrations
python manage.py migrate

Create a superuser
python manage.py createsuperuser

Run the development server
python manage.py runserver

Docker Setup

Build and start containers
docker-compose up --build

Access the API
The API is available at http://localhost:8000/api/
Swagger documentation is available at http://localhost:8000/swagger/

Notes

All API requests must include a valid X-API-Key header.

Admin panel is available at /admin/ to manage API keys, blocked entities, and subscription plans.

Redis caching is optional but can improve performance if enabled.

