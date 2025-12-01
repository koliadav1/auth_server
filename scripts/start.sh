#!/bin/bash

echo "Waiting for PostgreSQL..."
until pg_isready -h postgres -p 5432 -U $DB_USER; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 2
done
echo "PostgreSQL is ready!"

echo "Running database migrations..."
alembic upgrade head

echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000