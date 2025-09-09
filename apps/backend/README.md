# Visor Urbano Backend

This project constitutes the backend for the Visor Urbano application.

## System Requirements

- PostgreSQL@14
- Enable the PostGIS extension in PostgreSQL:
    ```sql
    CREATE EXTENSION postgis;
    ```
    OR 
    psql -U user -d dabtabase_name
    CREATE EXTENSION postgis;
- Python 3.11


## Installation

1. Install PostgreSQL version 14:
    - On macOS: `brew install postgresql@14` AND `brew install postgis`
    - On Ubuntu/Debian: use the official repository or follow PostgreSQL documentation

2. Clone the repository and navigate to the backend directory:
    ```
    git clone <repo-url>
    cd visor-urbano/apps/backend
    ```

3. Configure environment variables:
    - Create a `.env` file in the root directory with the necessary configuration (e.g., database connection details).

4. Create a virtual environment and install dependencies:
    ```
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
5. Run the migrations:
    - Create the first migration:
    ```    
    alembic revision --autogenerate -m "initial migration" 
    ```    
    - Apply the migration:
    ```    
    alembic upgrade head
    ```
6. Run the application:
    ```
    uvicorn app.main:app --reload
    ```    
## Usage

- Access the API documentation via Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## Missing PostGIS Extension Error
The error type "geometry" does not exist indicates that the PostGIS extension is not installed or enabled in your PostgreSQL database. Since your models use GeoAlchemy2 with spatial data types, you need PostGIS.

Solution: Install and Enable PostGIS
1. Install PostGIS (if not already installed):
brew install postgis

2. Enable PostGIS extension in your database:
Connect to your database and run:
psql -U visorurbano -d visorurbano_db

3.Then run the SQL command:
CREATE EXTENSION postgis;

4. Try the migration again:
alembic upgrade head
<br>
<hr />

# Docker Compose Setup Process for 'npm run dev'
When you run npm run dev in the Visor Urbano backend application, you're executing the script defined in package.json which runs docker compose up. This command orchestrates the setup and startup of the services defined in docker-compose.yaml.


## Docker Compose starts two services:

- db: A PostgreSQL database with PostGIS extension (using postgis/postgis:15-3.3 image)
- backend: The FastAPI application (built from the Dockerfile)

## Database setup:

- PostgreSQL starts with environment variables from your .env file
- The init-db.sh script runs to create PostGIS extensions
- A health check ensures the database is ready before proceeding

## Backend startup:

- Once the database is healthy, the backend container starts
- It first runs wait-for-db.sh to ensure the database connection works
- Then docker-backend.sh executes, which:
    - Checks if database tables exist
    - Creates and applies Alembic migrations as needed
    - Starts the FastAPI application with Uvicorn on port 8000

The backend will be accessible at http://localhost:8000 with API documentation available at http://localhost:8000/docs.

Both services use a Docker network called app_network to communicate, and the database data is persisted in a Docker volume called postgres_data.

## Please ensure update requirements.txt with the following packages from your virtual environment:
```
pip freeze > requirements.txt
```