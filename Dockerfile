
FROM python:3.11-slim as builder
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --prefix=/app/deps --no-cache-dir -r requirements.txt --verbose


FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/deps /usr/local
COPY . .
RUN mkdir -p uploads/chunks uploads/final
EXPOSE 5000
ENV FLASK_ENV=production
CMD ["python", "app.py"]
