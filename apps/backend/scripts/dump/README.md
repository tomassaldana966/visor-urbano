# Database Management Scripts

This directory contains scripts for managing the Visor Urbano database, including creating backups and setting up new development environments.

## Scripts Overview

### 1. `init_database.sh` - Database Initialization

Sets up a complete database environment for new developers.

**Usage:**
```bash
./init_database.sh
```

**What it does:**
- Checks PostgreSQL connectivity
- Creates the database if it doesn't exist
- Offers to restore from existing dumps
- Runs Alembic migrations to set up schema
- Optionally loads seed data
- Provides helpful next steps

**Prerequisites:**
- PostgreSQL server running and accessible
- Environment variables set (in `.env` file or exported)
- Python dependencies installed (`pip install -r requirements.txt`)

### 2. `create_db_dump.sh` - Database Backup

Creates comprehensive database backups for distribution and backup purposes.

**Usage:**
```bash
./create_db_dump.sh
```

**What it creates:**
- Schema-only dump (`visor_urbano_schema_TIMESTAMP.sql`)
- Data-only dump (`visor_urbano_data_TIMESTAMP.sql`)
- Full dump with schema and data (`visor_urbano_full_TIMESTAMP.sql`)
- Compressed versions of all dumps (`.gz` files)

**Output location:** `./database_dumps/`

## Environment Configuration

The scripts use the following environment variables:

```bash
DATABASE_HOST=localhost          # Database server host
DATABASE_PORT=5432              # Database server port
DATABASE_NAME=visor_urbano      # Database name
DATABASE_USERNAME=postgres      # Database username
DATABASE_PASSWORD=password      # Database password
```

These can be set in:
1. A `.env` file in the backend root directory
2. Exported as environment variables
3. The scripts will use defaults if not specified

## Typical Workflows

### For New Developers

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd visor-urbano/apps/backend
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env  # Edit with your database credentials
   pip install -r requirements.txt
   ```

3. **Initialize database:**
   ```bash
   cd scripts/dump
   ./init_database.sh
   ```

4. **Start development:**
   ```bash
   cd ../..
   ./startup.sh
   ```

### For Database Backups

1. **Create a backup:**
   ```bash
   cd scripts/dump
   ./create_db_dump.sh
   ```

2. **Share the dump:**
   - Use the compressed `.gz` files for smaller file sizes
   - Share the `visor_urbano_full_TIMESTAMP.sql.gz` for complete setup

### For Restoring from Backup

1. **Using init_database.sh (recommended):**
   ```bash
   # Place your dump file in ./database_dumps/
   ./init_database.sh
   # Follow prompts to restore from dump
   ```

2. **Manual restoration:**
   ```bash
   # Extract compressed dump if needed
   gunzip visor_urbano_full_TIMESTAMP.sql.gz
   
   # Restore to database
   psql -h localhost -U postgres -d visor_urbano < visor_urbano_full_TIMESTAMP.sql
   ```

## Troubleshooting

### PostgreSQL Connection Issues
- Ensure PostgreSQL is running: `pg_isready`
- Check connection parameters in `.env`
- Verify user permissions and password

### Migration Issues
- Check current migration status: `alembic current`
- View migration history: `alembic history`
- Reset to specific migration: `alembic downgrade <revision>`

### Permission Issues
- Ensure scripts are executable: `chmod +x *.sh`
- Check database user permissions
- Verify file system permissions for dump directory

## Database Schema Information

The Visor Urbano database includes:

- **Business Types**: Catalog of business classifications with SCIAN codes
- **Municipalities**: Geographic administrative divisions
- **Business Licenses**: License management and tracking
- **User Management**: Authentication and authorization
- **Procedures**: Administrative process management
- **Zoning**: Urban development and land use regulations

### Recent Schema Changes

- **Business Types Enhancement**: Added `code` (SCIAN) and `related_words` fields
- **English Translation**: Converted Spanish column names to English for better international compatibility
- **Migration History**: All changes tracked through Alembic migrations

## API Endpoints

After setup, the following key endpoints will be available:

- `GET /v1/business_types/enabled?municipality_id=1` - Get enabled business types
- `GET /docs` - Interactive API documentation
- `GET /v1/municipalities` - List municipalities

## Support

For issues with these scripts or database setup:

1. Check the troubleshooting section above
2. Review the application logs
3. Verify all prerequisites are met
4. Check that environment variables are correctly set
