#!/bin/bash
set -e

function wait_for_db() {
  echo "Waiting for database to be ready..."
  for i in {1..30}; do
    if docker exec db pg_isready -U ${DATABASE_USERNAME:-postgres}; then
      echo "Database is ready!"
      return
    fi
    echo "Waiting for database to start... ($i/30)"
    sleep 2
  done
  echo "Database failed to start." >&2
  exit 1
}

# Cleanup
echo "Stopping and removing Docker containers and volumes..."
docker-compose down --volumes --remove-orphans
docker volume prune -f

# Remove migrations
echo "Removing old migration files..."
rm -rf migrations/versions/*

# Start Database
echo "Starting database container..."
docker-compose up -d db

wait_for_db

echo "Creating and applying fresh migration..."
docker-compose run --rm backend bash -c "cd /app && alembic revision --autogenerate -m 'Initial fresh migration' && alembic upgrade head"

# Start all containers
echo "Starting all containers..."
docker-compose up -d

echo "Setup complete!"
