FROM python:3.10

WORKDIR /app

# Install system dependencies including SQLite
RUN apt-get update && apt-get install -y \
    postgresql-client \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run the application
CMD ["bash", "-c", "gunicorn config.wsgi:application --workers ${WEB_CONCURRENCY:-1} --bind 0.0.0.0:8080"]
