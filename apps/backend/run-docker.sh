#!/bin/bash
set -e

echo "Stopping Docker containers..."
docker-compose down --volumes --remove-orphans
docker volume prune -f
docker-compose rm -vf

echo "Removing old migration files..."
rm -rf migrations/versions/*

echo "Starting database container..."
docker-compose up -d db

echo "Waiting for database to be ready..."

for i in {1..30}; do
  if docker exec postgres_db pg_isready -U $DATABASE_USERNAME; then
    echo "Database is ready!"
    break
  fi
  echo "Waiting for database to start... ($i/30)"
  sleep 2
done

echo "Creating a fresh initial migration..."

docker-compose run --rm backend bash -c "cd /app && alembic revision --autogenerate -m 'Initial fresh migration'"

echo "Upgrading database with new migration..."
docker-compose run --rm backend bash -c "cd /app && alembic upgrade head"

echo "Migration reset complete!"
echo "Starting all containers..."
docker-compose up -d

echo "Setup complete!"