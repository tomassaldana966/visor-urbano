#!/bin/bash
set -e

host="$1"
port="$2"
user="$3"
password="$4"
database="$5"
max_attempts="$6"

if [ -z "$host" ] || [ -z "$port" ] || [ -z "$user" ] || [ -z "$database" ]; then
  echo "Usage: $0 <host> <port> <user> <password> <database> [max_attempts=60]"
  exit 1
fi

# Default to 60 attempts (5 minutes at 5 second intervals)
max_attempts=${max_attempts:-60}
attempt=0

echo "Waiting for PostgreSQL on $host:$port..."

# Export password for psql commands
export PGPASSWORD="$password"

until psql -h "$host" -p "$port" -U "$user" -d "$database" -c "SELECT 1" > /dev/null 2>&1; do
  attempt=$((attempt+1))
  echo "Waiting for PostgreSQL ($attempt/$max_attempts)..."
  
  if [ $attempt -ge $max_attempts ]; then
    echo "PostgreSQL did not become available in time."
    exit 1
  fi
  
  sleep 5
done

echo "PostgreSQL is now available"