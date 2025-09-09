#!/bin/bash

# Database dump script for Visor Urbano
# This script creates a complete database dump including schema and data

set -e

# Load environment variables
if [ -f ../../.env ]; then
    source ../../.env
fi

# Default values
DATABASE_HOST=${DATABASE_HOST:-localhost}
DATABASE_PORT=${DATABASE_PORT:-5432}
DATABASE_NAME=${DATABASE_NAME:-visor_urbano}
DATABASE_USERNAME=${DATABASE_USERNAME:-postgres}
DATABASE_PASSWORD=${DATABASE_PASSWORD:-password}

# Create dump directory if it doesn't exist
DUMP_DIR="./database_dumps"
mkdir -p "$DUMP_DIR"

# Get current timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Dump file names
SCHEMA_DUMP="$DUMP_DIR/visor_urbano_schema_$TIMESTAMP.sql"
DATA_DUMP="$DUMP_DIR/visor_urbano_data_$TIMESTAMP.sql"
FULL_DUMP="$DUMP_DIR/visor_urbano_full_$TIMESTAMP.sql"

echo "Creating database dumps..."
echo "Host: $DATABASE_HOST:$DATABASE_PORT"
echo "Database: $DATABASE_NAME"
echo "User: $DATABASE_USERNAME"

# Set password for pg_dump
export PGPASSWORD="$DATABASE_PASSWORD"

# Create schema-only dump
echo "Creating schema dump..."
pg_dump -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME" \
    --schema-only --no-owner --no-privileges \
    "$DATABASE_NAME" > "$SCHEMA_DUMP"

if [ $? -eq 0 ]; then
    echo "Schema dump created: $SCHEMA_DUMP"
else
    echo "Error creating schema dump"
    exit 1
fi

# Create data-only dump
echo "Creating data dump..."
pg_dump -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME" \
    --data-only --no-owner --no-privileges \
    --disable-triggers \
    "$DATABASE_NAME" > "$DATA_DUMP"

if [ $? -eq 0 ]; then
    echo "Data dump created: $DATA_DUMP"
else
    echo "Error creating data dump"
    exit 1
fi

# Create full dump (schema + data)
echo "Creating full dump..."
pg_dump -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME" \
    --no-owner --no-privileges \
    "$DATABASE_NAME" > "$FULL_DUMP"

if [ $? -eq 0 ]; then
    echo "Full dump created: $FULL_DUMP"
else
    echo "Error creating full dump"
    exit 1
fi

# Create compressed versions
echo "Creating compressed versions..."
gzip -c "$SCHEMA_DUMP" > "$SCHEMA_DUMP.gz"
gzip -c "$DATA_DUMP" > "$DATA_DUMP.gz"
gzip -c "$FULL_DUMP" > "$FULL_DUMP.gz"

echo ""
echo "Database dumps completed successfully!"
echo "Files created:"
echo "  - Schema: $SCHEMA_DUMP (.gz)"
echo "  - Data: $DATA_DUMP (.gz)"
echo "  - Full: $FULL_DUMP (.gz)"
echo ""
echo "To restore:"
echo "  Schema: psql -h host -U user -d database < $SCHEMA_DUMP"
echo "  Data: psql -h host -U user -d database < $DATA_DUMP"
echo "  Full: psql -h host -U user -d database < $FULL_DUMP"

# Unset password
unset PGPASSWORD
