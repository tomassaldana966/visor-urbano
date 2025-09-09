# GeoServer Setup Guide for Visor Urbano

This guide will walk you through setting up GeoServer from scratch to work perfectly with Visor Urbano. This guide covers installation, configuration, data preparation, and integration with the existing application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [GeoServer Installation](#geoserver-installation)
3. [Initial Configuration](#initial-configuration)
4. [PostgreSQL/PostGIS Setup](#postgresqlpostgis-setup)
5. [Data Store Configuration](#data-store-configuration)
6. [Layer Creation & Publishing](#layer-creation--publishing)
7. [Styling Configuration](#styling-configuration)
8. [Security Configuration](#security-configuration)
9. [Performance Optimization](#performance-optimization)
10. [Integration with Visor Urbano](#integration-with-visor-urbano)
11. [Testing & Validation](#testing--validation)
12. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Operating System**: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 20GB free space
- **Java**: OpenJDK 11 or Oracle JDK 11
- **Database**: PostgreSQL 12+ with PostGIS 3.0+

### Required Software

#### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Java 11
sudo apt install openjdk-11-jdk

# Install PostgreSQL with PostGIS
sudo apt install postgresql-12 postgresql-12-postgis-3 postgresql-contrib

# Install additional utilities
sudo apt install wget unzip curl
```

#### Linux (CentOS/RHEL)

```bash
# Install EPEL repository
sudo yum install epel-release

# Install Java 11
sudo yum install java-11-openjdk java-11-openjdk-devel

# Install PostgreSQL 12 with PostGIS
sudo yum install postgresql12-server postgresql12 postgis30_12

# Install additional utilities
sudo yum install wget unzip curl
```

#### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Java 11
brew install openjdk@11
echo 'export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Install PostgreSQL with PostGIS
brew install postgresql@12 postgis

# Start PostgreSQL service
brew services start postgresql@12

# Install additional utilities
brew install wget
```

#### Windows

1. **Download and Install Java 11**
   - Download OpenJDK 11 from [Eclipse Temurin](https://adoptium.net/)
   - Run the installer and follow the wizard
   - Verify installation: Open Command Prompt and run `java -version`

2. **Download and Install PostgreSQL with PostGIS**
   - Download PostgreSQL 12+ from [postgresql.org](https://www.postgresql.org/download/windows/)
   - During installation, make sure to include PostGIS in the Stack Builder
   - Set a strong password for the postgres user
   - Note the port (default: 5432)

3. **Install Additional Tools**
   - Download and install [Git for Windows](https://git-scm.com/download/win) (includes bash)
   - Optional: Install [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install) for better command-line experience

### Network Requirements

- **Port 8080**: GeoServer web interface
- **Port 5432**: PostgreSQL database
- **Port 80/443**: Web server (if using reverse proxy)

---

## GeoServer Installation

### Method 1: WAR File Installation (Recommended)

#### For Linux (Ubuntu/CentOS)

**Step 1: Download GeoServer**

```bash
# Create GeoServer directory
sudo mkdir -p /opt/geoserver
cd /opt/geoserver

# Download latest stable version (2.24.x as of 2024)
wget "https://sourceforge.net/projects/geoserver/files/GeoServer/2.24.1/geoserver-2.24.1-war.zip"

# Extract the archive
unzip geoserver-2.24.1-war.zip
```

**Step 2: Install Apache Tomcat**

```bash
# Install Tomcat 9
sudo apt install tomcat9 tomcat9-admin

# Or manually install:
wget "https://downloads.apache.org/tomcat/tomcat-9/v9.0.82/bin/apache-tomcat-9.0.82.tar.gz"
sudo tar -xzf apache-tomcat-9.0.82.tar.gz -C /opt/
sudo mv /opt/apache-tomcat-9.0.82 /opt/tomcat9
sudo chown -R tomcat:tomcat /opt/tomcat9
```

**Step 3: Deploy GeoServer**

```bash
# Copy WAR file to Tomcat webapps
sudo cp geoserver.war /var/lib/tomcat9/webapps/

# Set proper permissions
sudo chown tomcat:tomcat /var/lib/tomcat9/webapps/geoserver.war

# Restart Tomcat
sudo systemctl restart tomcat9
sudo systemctl enable tomcat9
```

#### For macOS

**Step 1: Download GeoServer**

```bash
# Create GeoServer directory
mkdir -p ~/geoserver
cd ~/geoserver

# Download latest stable version
curl -L "https://sourceforge.net/projects/geoserver/files/GeoServer/2.24.1/geoserver-2.24.1-war.zip" -o geoserver-2.24.1-war.zip

# Extract the archive
unzip geoserver-2.24.1-war.zip
```

**Step 2: Install Apache Tomcat**

```bash
# Install Tomcat via Homebrew
brew install tomcat

# Or manually download and install:
curl -L "https://downloads.apache.org/tomcat/tomcat-9/v9.0.82/bin/apache-tomcat-9.0.82.tar.gz" -o tomcat.tar.gz
tar -xzf tomcat.tar.gz
mv apache-tomcat-9.0.82 /usr/local/tomcat9
```

**Step 3: Deploy GeoServer**

```bash
# Copy WAR file to Tomcat webapps
cp geoserver.war /usr/local/var/lib/tomcat/webapps/
# Or if manually installed:
cp geoserver.war /usr/local/tomcat9/webapps/

# Start Tomcat
brew services start tomcat
# Or if manually installed:
/usr/local/tomcat9/bin/startup.sh
```

#### For Windows

**Step 1: Download GeoServer**

1. Open PowerShell as Administrator
2. Create directory and download:

```powershell
# Create GeoServer directory
New-Item -ItemType Directory -Force -Path "C:\geoserver"
Set-Location "C:\geoserver"

# Download GeoServer (using PowerShell 5+)
Invoke-WebRequest -Uri "https://sourceforge.net/projects/geoserver/files/GeoServer/2.24.1/geoserver-2.24.1-war.zip" -OutFile "geoserver-2.24.1-war.zip"

# Extract (requires PowerShell 5+ or 7-Zip)
Expand-Archive -Path "geoserver-2.24.1-war.zip" -DestinationPath "."
```

**Step 2: Install Apache Tomcat**

1. Download Tomcat 9 from [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
2. Choose "32-bit/64-bit Windows Service Installer"
3. Run the installer with these settings:
   - Installation Directory: `C:\Program Files\Apache Software Foundation\Tomcat 9.0`
   - Port: `8080`
   - Create Windows Service: Yes
   - Start service after installation: Yes

**Step 3: Deploy GeoServer**

```powershell
# Copy WAR file to Tomcat webapps
Copy-Item "geoserver.war" -Destination "C:\Program Files\Apache Software Foundation\Tomcat 9.0\webapps\"

# Restart Tomcat service
Restart-Service Tomcat9

# Or using GUI: Services.msc → Find "Apache Tomcat 9.0 Tomcat9" → Restart
```

**Alternative: Using Windows Subsystem for Linux (WSL)**

If you have WSL installed, you can follow the Linux instructions:

```bash
# In WSL terminal
wsl

# Follow the Linux installation steps above
# GeoServer will be accessible at http://localhost:8080/geoserver
```

### Method 2: Docker Installation (Cross-Platform)

This method works identically on Linux, macOS, and Windows:

**Prerequisites**: Install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)

```bash
# Create data directory
mkdir -p ./geoserver-data

# Run GeoServer container
docker run -d \
  --name geoserver \
  -p 8080:8080 \
  -v $(pwd)/geoserver-data:/opt/geoserver/data_dir \
  -e GEOSERVER_ADMIN_PASSWORD=mySecurePassword \
  kartoza/geoserver:2.24.0

# Or using docker-compose (create docker-compose.yml)
```

**Docker Compose file (docker-compose.yml)**:

```yaml
version: '3.8'
services:
  geoserver:
    image: kartoza/geoserver:2.24.0
    container_name: geoserver
    restart: unless-stopped
    ports:
      - '8080:8080'
    volumes:
      - ./geoserver-data:/opt/geoserver/data_dir
    environment:
      - GEOSERVER_ADMIN_PASSWORD=mySecurePassword
      - JAVA_OPTS=-Xms512m -Xmx2g

  postgres:
    image: postgis/postgis:12-3.0
    container_name: geoserver-db
    restart: unless-stopped
    ports:
      - '5432:5432'
    environment:
      - POSTGRES_DB=visor_urbano
      - POSTGRES_USER=gis_user
      - POSTGRES_PASSWORD=gis_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
# Start services
docker-compose up -d
```

### Step 4: Verify Installation (All Platforms)

**Using Command Line:**

```bash
# Check if GeoServer is running
curl http://localhost:8080/geoserver

# Windows PowerShell alternative:
Invoke-WebRequest -Uri "http://localhost:8080/geoserver"
```

**Using Web Browser:**

1. Open your browser
2. Navigate to `http://localhost:8080/geoserver`
3. Login with:
   - Username: `admin`
   - Password: `geoserver` (default) or your custom password

**Check Logs:**

```bash
# Linux
sudo tail -f /var/log/tomcat9/catalina.out

# macOS (Homebrew)
tail -f /usr/local/var/log/tomcat/catalina.out

# Windows (check in Event Viewer or Tomcat logs directory)
# C:\Program Files\Apache Software Foundation\Tomcat 9.0\logs\catalina.out

# Docker (any platform)
docker logs -f geoserver
```

---

## Initial Configuration

### Step 1: Access GeoServer Web Interface

1. Open your browser and navigate to: `http://your-server:8080/geoserver`
2. Click on "Login" in the top right corner
3. Use default credentials:
   - **Username**: `admin`
   - **Password**: `geoserver`

### Step 2: Change Default Password

1. Go to **Security** → **Users, Groups, and Roles**
2. Click on **Users/Groups** tab
3. Click on **admin** user
4. Change the password to a secure one
5. Save changes

### Step 3: Configure Global Settings

1. Go to **Settings** → **Global**
2. Configure the following:

```properties
# Global Settings
Verbose Messages: Enable
Verbose Exception Reporting: Enable (for development)
Character Set: UTF-8
Number of Decimals: 6
Online Resource: http://your-domain.com/geoserver

# JAI Settings
JAI Memory Capacity: 0.5
JAI Memory Threshold: 0.75
JAI Tile Threads: 7
JAI Tile Priority: 5

# Coverage Access Settings
ImageIO Cache Memory Threshold: 10240
```

### Step 4: Configure Logging

1. Go to **Settings** → **Global**
2. Set logging profile to **VERBOSE_LOGGING**
3. Configure log location: `/opt/geoserver/logs/geoserver.log`

---

## PostgreSQL/PostGIS Setup

### Step 1: Install and Configure PostgreSQL

#### For Linux (Ubuntu/Debian)

```bash
# Install PostgreSQL 12 with PostGIS
sudo apt update
sudo apt install postgresql-12 postgresql-12-postgis-3 postgresql-contrib

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE visor_urbano;
CREATE USER gis_user WITH PASSWORD 'gis_password';
GRANT ALL PRIVILEGES ON DATABASE visor_urbano TO gis_user;
\q
```

#### For Linux (CentOS/RHEL)

```bash
# Install PostgreSQL 12 repository
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Install PostgreSQL 12 with PostGIS
sudo yum install -y postgresql12-server postgresql12 postgis30_12

# Initialize database
sudo /usr/pgsql-12/bin/postgresql-12-setup initdb

# Start and enable PostgreSQL
sudo systemctl start postgresql-12
sudo systemctl enable postgresql-12

# Create database and user
sudo -u postgres psql
CREATE DATABASE visor_urbano;
CREATE USER gis_user WITH PASSWORD 'gis_password';
GRANT ALL PRIVILEGES ON DATABASE visor_urbano TO gis_user;
\q
```

#### For macOS

```bash
# PostgreSQL should already be installed from Prerequisites
# If not, install it:
brew install postgresql@12 postgis

# Start PostgreSQL
brew services start postgresql@12

# Create database and user
psql postgres
CREATE DATABASE visor_urbano;
CREATE USER gis_user WITH PASSWORD 'gis_password';
GRANT ALL PRIVILEGES ON DATABASE visor_urbano TO gis_user;
\q
```

#### For Windows

**Using pgAdmin (Recommended for Windows):**

1. PostgreSQL should be installed from Prerequisites
2. Open pgAdmin 4 from Start Menu
3. Connect to local PostgreSQL server (password set during installation)
4. Right-click "Databases" → "Create" → "Database"
   - Name: `visor_urbano`
   - Owner: `postgres`
5. Right-click "Login/Group Roles" → "Create" → "Login/Group Role"
   - Name: `gis_user`
   - Password: `gis_password`
   - Privileges: Can login? Yes
6. Right-click `visor_urbano` database → "Properties" → "Security"
   - Add `gis_user` with all privileges

**Using Command Line (if psql is in PATH):**

```cmd
REM Open Command Prompt as Administrator
psql -U postgres
CREATE DATABASE visor_urbano;
CREATE USER gis_user WITH PASSWORD 'gis_password';
GRANT ALL PRIVILEGES ON DATABASE visor_urbano TO gis_user;
\q
```

### Step 2: Enable PostGIS Extension

#### All Platforms

```sql
-- Connect to the visor_urbano database
-- Linux/macOS:
sudo -u postgres psql -d visor_urbano
-- Windows (pgAdmin or psql):
psql -U postgres -d visor_urbano

-- Enable PostGIS extension
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;

-- Verify installation
SELECT PostGIS_Version();

-- Grant permissions to gis_user
GRANT ALL ON spatial_ref_sys TO gis_user;
GRANT ALL ON geometry_columns TO gis_user;
\q
```

### Step 3: Configure PostgreSQL for Performance

#### For Linux

```bash
# Edit postgresql.conf
sudo nano /etc/postgresql/12/main/postgresql.conf

# Add/modify these settings:
listen_addresses = '*'
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

# Edit pg_hba.conf for authentication
sudo nano /etc/postgresql/12/main/pg_hba.conf

# Add this line for local connections:
host    visor_urbano    gis_user    127.0.0.1/32    md5
host    visor_urbano    gis_user    ::1/128         md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### For macOS

```bash
# Find PostgreSQL config location
brew --prefix postgresql@12

# Edit postgresql.conf (usually in /usr/local/var/postgresql@12/)
nano /usr/local/var/postgresql@12/postgresql.conf

# Add/modify these settings:
listen_addresses = '*'
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

# Edit pg_hba.conf
nano /usr/local/var/postgresql@12/pg_hba.conf

# Add authentication line:
host    visor_urbano    gis_user    127.0.0.1/32    md5
host    visor_urbano    gis_user    ::1/128         md5

# Restart PostgreSQL
brew services restart postgresql@12
```

#### For Windows

1. **Find PostgreSQL installation directory** (usually `C:\Program Files\PostgreSQL\12\`)
2. **Edit postgresql.conf**:
   - Open `C:\Program Files\PostgreSQL\12\data\postgresql.conf` in Notepad (as Administrator)
   - Modify these settings:
   ```
   listen_addresses = '*'
   max_connections = 200
   shared_buffers = 256MB
   effective_cache_size = 1GB
   work_mem = 4MB
   maintenance_work_mem = 64MB
   ```
3. **Edit pg_hba.conf**:
   - Open `C:\Program Files\PostgreSQL\12\data\pg_hba.conf` in Notepad (as Administrator)
   - Add these lines:
   ```
   host    visor_urbano    gis_user    127.0.0.1/32    md5
   host    visor_urbano    gis_user    ::1/128         md5
   ```
4. **Restart PostgreSQL service**:
   - Open Services.msc
   - Find "postgresql-x64-12" service
   - Right-click → Restart

### Step 4: Optimize PostGIS for Performance

```sql
-- Connect to database (all platforms)
-- Linux/macOS: sudo -u postgres psql -d visor_urbano
-- Windows: psql -U postgres -d visor_urbano

-- Optimize PostgreSQL settings for spatial data
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET checkpoint_completion_target = 0.9;

-- Reload configuration
SELECT pg_reload_conf();
\q
```

---

## Data Store Configuration

### Step 1: Create PostgreSQL Data Store

1. In GeoServer admin interface, go to **Stores** → **Add new Store**
2. Select **PostGIS - PostGIS Database**
3. Configure the data store:

```properties
# Basic Store Info
Workspace: visor (create if doesn't exist)
Data Source Name: visor_postgis
Description: Visor Urbano PostGIS Database

# Connection Parameters
host: localhost
port: 5432
database: visor_urbano
schema: public
user: gis_user
passwd: gis_password

# Connection pool settings
min connections: 1
max connections: 10
fetch size: 1000
Connection timeout: 20
validate connections: true

# Advanced settings
Loose bbox: true
Prepared statements: true
Estimated extends: false
```

4. Click **Save**

### Step 2: Test Connection

1. Click **Test Connection** to verify the setup
2. You should see "Connection successful"

---

## Layer Creation & Publishing

### Step 1: Prepare Sample Data

For this example, we'll create the essential layers that Visor Urbano expects:

```sql
-- Connect to database
sudo -u postgres psql -d visor_urbano

-- Create municipalities table
CREATE TABLE municipios (
    id SERIAL PRIMARY KEY,
    nom_mun VARCHAR(100) NOT NULL,
    geom GEOMETRY(MultiPolygon, 4326)
);

-- Create states table
CREATE TABLE estados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    geom GEOMETRY(MultiPolygon, 4326)
);

-- Create properties table (predios)
CREATE TABLE predios (
    id SERIAL PRIMARY KEY,
    fid INTEGER,
    AGUA_POT VARCHAR(50),
    ALUMBRADO VARCHAR(50),
    BASURA VARCHAR(50),
    CAL_POS VARCHAR(50),
    CLAS_EQUIP VARCHAR(50),
    CLAS_TEN VARCHAR(50),
    CP VARCHAR(10),
    CVE_CAT VARCHAR(50),
    CVE_STD VARCHAR(50),
    DRENAJE VARCHAR(50),
    ENCARGADO VARCHAR(100),
    FOLIO_REAL VARCHAR(50),
    FUENTE VARCHAR(50),
    LAT VARCHAR(20),
    LON VARCHAR(20),
    LUZ VARCHAR(50),
    municipio_id INTEGER,
    NOM_AH VARCHAR(100),
    NOM_ENT VARCHAR(100),
    NOM_EQUIP VARCHAR(100),
    NOM_LOC VARCHAR(100),
    NOM_MUN VARCHAR(100),
    NOM_REG VARCHAR(100),
    NOM_VIAL VARCHAR(200),
    NOM_ZNA VARCHAR(100),
    NUM_EXT VARCHAR(20),
    NUM_INT VARCHAR(20),
    OBJECTID INTEGER,
    PAVIMENTO VARCHAR(50),
    SUP_CONST NUMERIC,
    SUP_TOT NUMERIC,
    TIPO_ASEN VARCHAR(50),
    TIPO_EQUIP VARCHAR(50),
    TIPO_TEN VARCHAR(50),
    TIPO_VIAL VARCHAR(50),
    TOT_PROP VARCHAR(50),
    geom GEOMETRY(MultiPolygon, 4326)
);

-- Create spatial indexes
CREATE INDEX idx_municipios_geom ON municipios USING GIST (geom);
CREATE INDEX idx_estados_geom ON estados USING GIST (geom);
CREATE INDEX idx_predios_geom ON predios USING GIST (geom);
CREATE INDEX idx_predios_municipio_id ON predios (municipio_id);

-- Insert sample data for Chihuahua (Mexico example)
INSERT INTO estados (nombre, geom) VALUES
('Chihuahua', ST_GeomFromText('POLYGON((-109 25, -103 25, -103 32, -109 32, -109 25))', 4326));

INSERT INTO municipios (nom_mun, geom) VALUES
('Chihuahua', ST_GeomFromText('POLYGON((-106.5 28.2, -105.5 28.2, -105.5 29.2, -106.5 29.2, -106.5 28.2))', 4326));

-- Insert sample property (you'll replace this with real data)
INSERT INTO predios (
    fid, municipio_id, NOM_MUN, NOM_LOC, NOM_VIAL, NUM_EXT,
    SUP_TOT, SUP_CONST, LAT, LON, geom
) VALUES (
    1, 1, 'Chihuahua', 'Chihuahua', 'Calle Principal', '123',
    500.00, 200.00, '28.6353', '-106.0889',
    ST_GeomFromText('POLYGON((-106.089 28.635, -106.088 28.635, -106.088 28.636, -106.089 28.636, -106.089 28.635))', 4326)
);

-- Insert sample data for Maipú, Chile
INSERT INTO estados (nombre, geom) VALUES
('Región Metropolitana de Santiago', ST_GeomFromText('POLYGON((-72 -35, -69 -35, -69 -32, -72 -32, -72 -35))', 4326));

INSERT INTO municipios (nom_mun, geom) VALUES
('Maipú', ST_GeomFromText('POLYGON((-70.8 -33.6, -70.6 -33.6, -70.6 -33.4, -70.8 -33.4, -70.8 -33.6))', 4326));

-- Insert sample properties for Maipú
INSERT INTO predios (
    fid, municipio_id, NOM_MUN, NOM_LOC, NOM_VIAL, NUM_EXT,
    SUP_TOT, SUP_CONST, LAT, LON, geom
) VALUES
(
    2, 2, 'Maipú', 'Maipú Centro', 'Avenida Pajaritos', '4567',
    350.00, 180.00, '-33.5100', '-70.7594',
    ST_GeomFromText('POLYGON((-70.7595 -33.5101, -70.7593 -33.5101, -70.7593 -33.5099, -70.7595 -33.5099, -70.7595 -33.5101))', 4326)
),
(
    3, 2, 'Maipú', 'Villa Los Héroes', 'Calle Tres Poniente', '890',
    280.00, 120.00, '-33.5245', '-70.7512',
    ST_GeomFromText('POLYGON((-70.7513 -33.5246, -70.7511 -33.5246, -70.7511 -33.5244, -70.7513 -33.5244, -70.7513 -33.5246))', 4326)
),
(
    4, 2, 'Maipú', 'Rinconada de Maipú', 'Avenida Américo Vespucio', '1234',
    450.00, 220.00, '-33.5350', '-70.7200',
    ST_GeomFromText('POLYGON((-70.7201 -33.5351, -70.7199 -33.5351, -70.7199 -33.5349, -70.7201 -33.5349, -70.7201 -33.5351))', 4326)
);
```

### Step 2: Create Workspace

1. Go to **Workspaces** → **Add new workspace**
2. Configure:
   - **Name**: `visor`
   - **Namespace URI**: `http://visor.urbano.mx`
   - **Default**: Check this box
3. Click **Save**

### Step 3: Publish Layers

#### A. Publish Estados Layer

1. Go to **Layers** → **Add a new layer**
2. Select **visor:visor_postgis** data store
3. Click **Publish** next to `estados`
4. Configure layer:

```properties
# Basic Info
Name: estados
Title: Estados de México
Abstract: Layer containing state boundaries

# Coordinate Reference Systems
Native SRS: EPSG:4326
Declared SRS: EPSG:4326
SRS handling: Force declared

# Bounding Boxes
Native Bounding Box: Compute from data
Lat/Lon Bounding Box: Compute from native bounds
```

5. Go to **Publishing** tab:

```properties
# WMS Settings
Queryable: true
Opaque: false
Default Style: polygon

# WFS Settings
Per-request feature limit: 1000000
Maximum number of decimals: 6
```

6. Click **Save**

#### B. Publish Municipios Layer

Repeat the same process for municipalities:

1. **Layers** → **Add a new layer** → **visor:visor_postgis** → **Publish** `municipios`
2. Configure similar to estados layer
3. Set **Queryable**: true
4. **Save**

#### C. Publish Predios Layer

1. **Layers** → **Add a new layer** → **visor:visor_postgis** → **Publish** `predios`
2. Configure:

```properties
# Basic Info
Name: predios
Title: Predios Urbanos
Abstract: Urban properties with cadastral information

# CRS
Native SRS: EPSG:4326
Declared SRS: EPSG:4326

# WMS Settings
Queryable: true
Opaque: false
Default Style: polygon

# WFS Settings
Per-request feature limit: 50000
Maximum number of decimals: 8
```

3. **Save**

### Step 4: Configuration Examples for Chilean Municipalities (Maipú)

If you're setting up Visor Urbano for Chilean municipalities like Maipú, here are specific configurations:

#### A. Chilean Coordinate Reference System

Chile commonly uses:

- **EPSG:4326** (WGS84) for general purposes
- **EPSG:32719** (UTM Zone 19S) for precise measurements
- **EPSG:5361** (SIRGAS-Chile 2002 / UTM zone 19S) for official Chilean cartography

Configure layers for Chilean data:

```properties
# For Maipú/Santiago Metropolitan Region
Native SRS: EPSG:32719
Declared SRS: EPSG:32719
SRS handling: Force declared

# Alternative: Use SIRGAS-Chile for official data
Native SRS: EPSG:5361
Declared SRS: EPSG:5361
```

#### B. Chilean Administrative Boundaries

Create additional tables for Chilean administrative structure:

```sql
-- Create Chilean regions table
CREATE TABLE regiones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo_region VARCHAR(5) NOT NULL,
    geom GEOMETRY(MultiPolygon, 32719)
);

-- Create Chilean comunas table (equivalent to municipios)
CREATE TABLE comunas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo_comuna VARCHAR(10) NOT NULL,
    region_id INTEGER REFERENCES regiones(id),
    geom GEOMETRY(MultiPolygon, 32719)
);

-- Create Chilean properties table with local attributes
CREATE TABLE propiedades_chile (
    id SERIAL PRIMARY KEY,
    rol VARCHAR(20) UNIQUE NOT NULL, -- Chilean property ID
    sub_rol VARCHAR(10),
    direccion VARCHAR(200),
    numero VARCHAR(20),
    comuna_id INTEGER REFERENCES comunas(id),
    superficie_terreno NUMERIC(10,2),
    superficie_construida NUMERIC(10,2),
    avaluo_fiscal NUMERIC(12,0),
    ano_construccion INTEGER,
    destino VARCHAR(100),
    material_estructura VARCHAR(50),
    geom GEOMETRY(MultiPolygon, 32719)
);

-- Insert Maipú specific data
INSERT INTO regiones (nombre, codigo_region, geom) VALUES
('Región Metropolitana de Santiago', 'RM',
 ST_Transform(ST_GeomFromText('POLYGON((-72 -35, -69 -35, -69 -32, -72 -32, -72 -35))', 4326), 32719));

INSERT INTO comunas (nombre, codigo_comuna, region_id, geom) VALUES
('Maipú', '13110', 1,
 ST_Transform(ST_GeomFromText('POLYGON((-70.8 -33.6, -70.6 -33.6, -70.6 -33.4, -70.8 -33.4, -70.8 -33.6))', 4326), 32719));

-- Insert sample properties for Maipú neighborhoods
INSERT INTO propiedades_chile (
    rol, direccion, numero, comuna_id, superficie_terreno, superficie_construida,
    avaluo_fiscal, ano_construccion, destino, material_estructura, geom
) VALUES
('12345-6', 'Avenida Pajaritos', '4567', 1, 350.00, 180.00, 45000000, 2010, 'Habitacional', 'Hormigón Armado',
 ST_Transform(ST_GeomFromText('POLYGON((-70.7595 -33.5101, -70.7593 -33.5101, -70.7593 -33.5099, -70.7595 -33.5099, -70.7595 -33.5101))', 4326), 32719)),
('12346-4', 'Calle Tres Poniente', '890', 1, 280.00, 120.00, 38000000, 2005, 'Habitacional', 'Albañilería',
 ST_Transform(ST_GeomFromText('POLYGON((-70.7513 -33.5246, -70.7511 -33.5246, -70.7511 -33.5244, -70.7513 -33.5244, -70.7513 -33.5246))', 4326), 32719)),
('12347-2', 'Avenida Américo Vespucio', '1234', 1, 450.00, 220.00, 62000000, 2015, 'Habitacional', 'Hormigón Armado',
 ST_Transform(ST_GeomFromText('POLYGON((-70.7201 -33.5351, -70.7199 -33.5351, -70.7199 -33.5349, -70.7201 -33.5349, -70.7201 -33.5351))', 4326), 32719));

-- Create indexes for performance
CREATE INDEX idx_regiones_geom ON regiones USING GIST (geom);
CREATE INDEX idx_comunas_geom ON comunas USING GIST (geom);
CREATE INDEX idx_propiedades_chile_geom ON propiedades_chile USING GIST (geom);
CREATE INDEX idx_propiedades_chile_rol ON propiedades_chile (rol);
CREATE INDEX idx_propiedades_chile_comuna ON propiedades_chile (comuna_id);
```

#### C. Publish Chilean Layers

1. **Publish Regiones Layer**:
   - Name: `regiones`
   - Title: `Regiones de Chile`
   - CRS: `EPSG:32719`

2. **Publish Comunas Layer**:
   - Name: `comunas`
   - Title: `Comunas de Chile`
   - CRS: `EPSG:32719`

3. **Publish Propiedades Layer**:
   - Name: `propiedades_chile`
   - Title: `Propiedades de Chile`
   - CRS: `EPSG:32719`

#### D. Chilean-specific Environment Variables

For Visor Urbano configuration with Chilean data:

```bash
# Chilean configuration
MAP_ESTADO_LAYER=regiones
MAP_MUNICIPIO_LAYER=comunas
MAP_PREDIOS_LAYER=propiedades_chile
MAP_ESTADO_CQL_FILTER=nombre='Región Metropolitana de Santiago'
MAP_MUNICIPIO_CQL_FILTER=nombre='Maipú'

# Chilean coordinate system
MAP_DEFAULT_PROJECTION=EPSG:32719
MAP_CENTER_LAT=-33.5100
MAP_CENTER_LNG=-70.7594
MAP_DEFAULT_ZOOM=13

# Maipú specific bounds
MAP_BOUNDS_SOUTH=-33.6
MAP_BOUNDS_NORTH=-33.4
MAP_BOUNDS_WEST=-70.8
MAP_BOUNDS_EAST=-70.6
```

---

## Styling Configuration

### Step 1: Create Basic Polygon Style

1. Go to **Styles** → **Add a new style**
2. Create a style for properties:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld"
                         xmlns:sld="http://www.opengis.net/sld"
                         xmlns:ogc="http://www.opengis.net/ogc"
                         xmlns:gml="http://www.opengis.net/gml"
                         version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>predios_style</sld:Name>
    <sld:UserStyle>
      <sld:Name>predios_style</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:Name>Property Boundaries</sld:Name>
          <sld:PolygonSymbolizer>
            <sld:Fill>
              <sld:CssParameter name="fill">#FFFF99</sld:CssParameter>
              <sld:CssParameter name="fill-opacity">0.3</sld:CssParameter>
            </sld:Fill>
            <sld:Stroke>
              <sld:CssParameter name="stroke">#FF6600</sld:CssParameter>
              <sld:CssParameter name="stroke-width">2</sld:CssParameter>
              <sld:CssParameter name="stroke-opacity">0.8</sld:CssParameter>
            </sld:Stroke>
          </sld:PolygonSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>
```

3. Save as **predios_style**

### Step 2: Create Municipality Style

Create a style for municipalities:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld"
                         xmlns:sld="http://www.opengis.net/sld"
                         xmlns:ogc="http://www.opengis.net/ogc"
                         xmlns:gml="http://www.opengis.net/gml"
                         version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>municipios_style</sld:Name>
    <sld:UserStyle>
      <sld:Name>municipios_style</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:Name>Municipality Boundaries</sld:Name>
          <sld:PolygonSymbolizer>
            <sld:Fill>
              <sld:CssParameter name="fill">#E6F3FF</sld:CssParameter>
              <sld:CssParameter name="fill-opacity">0.2</sld:CssParameter>
            </sld:Fill>
            <sld:Stroke>
              <sld:CssParameter name="stroke">#0066CC</sld:CssParameter>
              <sld:CssParameter name="stroke-width">3</sld:CssParameter>
              <sld:CssParameter name="stroke-dasharray">10 5</sld:CssParameter>
            </sld:Stroke>
          </sld:PolygonSymbolizer>
          <sld:TextSymbolizer>
            <sld:Label>
              <ogc:PropertyName>nom_mun</ogc:PropertyName>
            </sld:Label>
            <sld:Font>
              <sld:CssParameter name="font-family">Arial</sld:CssParameter>
              <sld:CssParameter name="font-size">14</sld:CssParameter>
              <sld:CssParameter name="font-weight">bold</sld:CssParameter>
            </sld:Font>
            <sld:Fill>
              <sld:CssParameter name="fill">#0066CC</sld:CssParameter>
            </sld:Fill>
          </sld:TextSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>
```

### Step 3: Apply Styles to Layers

1. Go to **Layers** → Select your layer → **Publishing** tab
2. Change **Default Style** to your custom style
3. **Save**

---

## Security Configuration

### Step 1: Configure Service Security

1. Go to **Security** → **Services**
2. Configure access rules:

```properties
# Service-level security
*.*.r=*
*.*.w=ADMIN
wfs.*.r=*
wfs.*.w=ADMIN
wms.*.r=*
wms.*.w=ADMIN
```

### Step 2: Configure Data Security

1. Go to **Security** → **Data**
2. Add data access rules:

```properties
# Layer-level security
visor.*.r=*
visor.*.w=ADMIN
visor.predios.r=*
visor.predios.w=ADMIN
visor.municipios.r=*
visor.municipios.w=ADMIN
visor.estados.r=*
visor.estados.w=ADMIN
```

### Step 3: CORS Configuration

For web applications, configure CORS:

1. Edit **web.xml** in GeoServer:

```xml
<!-- Add CORS filter -->
<filter>
    <filter-name>CorsFilter</filter-name>
    <filter-class>org.apache.catalina.filters.CorsFilter</filter-class>
    <init-param>
        <param-name>cors.allowed.origins</param-name>
        <param-value>*</param-value>
    </init-param>
    <init-param>
        <param-name>cors.allowed.methods</param-name>
        <param-value>GET,POST,HEAD,OPTIONS,PUT</param-value>
    </init-param>
    <init-param>
        <param-name>cors.allowed.headers</param-name>
        <param-value>Content-Type,X-Requested-With,accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers</param-value>
    </init-param>
</filter>

<filter-mapping>
    <filter-name>CorsFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

---

## Performance Optimization

### Step 1: Configure Memory Settings

Edit Tomcat startup script to increase memory:

```bash
# Edit /etc/default/tomcat9
sudo nano /etc/default/tomcat9

# Add/modify JAVA_OPTS
JAVA_OPTS="-Djava.awt.headless=true -Xmx2048m -XX:+UseConcMarkSweepGC"

# For GeoServer specific settings
GEOSERVER_OPTS="-DGEOSERVER_DATA_DIR=/opt/geoserver/data_dir"
JAVA_OPTS="$JAVA_OPTS $GEOSERVER_OPTS"
```

### Step 2: Configure Tile Caching

1. Go to **Tile Caching** → **Caching Defaults**
2. Enable caching for your layers:

```properties
# Grid Sets
EPSG:4326: Enable
EPSG:900913: Enable (Web Mercator)

# Cache Configuration
Default cache format: image/png
Cache non-standard requests: false
Cache headers: true
```

3. Go to **Tile Caching** → **Tile Layers**
4. Configure caching for each layer:
   - **predios**: Enable with zoom levels 10-18
   - **municipios**: Enable with zoom levels 5-15
   - **estados**: Enable with zoom levels 3-10

### Step 3: Database Connection Optimization

Optimize the PostGIS data store:

```properties
# Connection Pool Settings
min connections: 2
max connections: 20
fetch size: 1000
Connection timeout: 30
validate connections: true
Test while idle: true
Time between eviction runs: 300
Min evictable time: 300
```

---

## Integration with Visor Urbano

### Step 1: Configure Environment Variables

#### For Mexican Municipalities (Chihuahua Example)

```bash
# .env file for Visor Urbano - Mexican Configuration
GEOSERVER_URL=http://your-geoserver-domain:8080/geoserver

# Layer names (matching what you created)
MAP_PREDIOS_LAYER=visor:predios
MAP_MUNICIPIO_LAYER=visor:municipios
MAP_ESTADO_LAYER=visor:estados
MAP_ESTADO_CQL_FILTER=nombre='Chihuahua'

# Map configuration for Chihuahua, Mexico
MAP_CENTER_LAT=28.6353
MAP_CENTER_LON=-106.0889
MAP_DEFAULT_ZOOM=12
MAP_TILE_CENTER_X=128
MAP_TILE_CENTER_Y=128

# Coordinate system
MAP_DEFAULT_PROJECTION=EPSG:32613
MAP_DISPLAY_PROJECTION=EPSG:4326

# Base layers for minimap
MAP_CROQUIS_BASE=visor:base_layer
```

#### For Chilean Municipalities (Maipú Example)

```bash
# .env file for Visor Urbano - Chilean Configuration
GEOSERVER_URL=http://your-geoserver-domain:8080/geoserver

# Layer names for Chilean administrative structure
MAP_PREDIOS_LAYER=visor:propiedades_chile
MAP_MUNICIPIO_LAYER=visor:comunas
MAP_ESTADO_LAYER=visor:regiones
MAP_ESTADO_CQL_FILTER=nombre='Región Metropolitana de Santiago'
MAP_MUNICIPIO_CQL_FILTER=nombre='Maipú'

# Map configuration for Maipú, Chile
MAP_CENTER_LAT=-33.5100
MAP_CENTER_LON=-70.7594
MAP_DEFAULT_ZOOM=13
MAP_TILE_CENTER_X=128
MAP_TILE_CENTER_Y=128

# Chilean coordinate system
MAP_DEFAULT_PROJECTION=EPSG:32719
MAP_DISPLAY_PROJECTION=EPSG:4326

# Bounds for Maipú
MAP_BOUNDS_SOUTH=-33.6
MAP_BOUNDS_NORTH=-33.4
MAP_BOUNDS_WEST=-70.8
MAP_BOUNDS_EAST=-70.6

# Chilean-specific fields
MAP_PROPERTY_ID_FIELD=rol
MAP_PROPERTY_SUBID_FIELD=sub_rol
MAP_ADDRESS_FIELD=direccion
MAP_SURFACE_FIELD=superficie_terreno
MAP_CONSTRUCTION_FIELD=superficie_construida
```

### Step 2: Update Backend Layer Configuration

#### Mexican Layers Configuration

```python
# apps/backend/scripts/seed_map_layers.py - Mexican Layers
MEXICO_LAYERS_DATA = [
    {
        "id": 1,
        "value": "predios_mexico",
        "label": "Predios Urbanos México",
        "type": "wms",
        "url": "http://your-geoserver:8080/geoserver/visor/wms",
        "layers": "visor:predios",
        "visible": True,
        "active": True,
        "attribution": "Visor Urbano México",
        "opacity": 1,
        "server_type": "geoserver",
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 1,
        "editable": True,
        "type_geom": "MultiPolygon",
        "cql_filter": None,
        "municipality": [1]  # Chihuahua municipality
    },
    {
        "id": 2,
        "value": "municipios_mexico",
        "label": "Municipios México",
        "type": "wms",
        "url": "http://your-geoserver:8080/geoserver/visor/wms",
        "layers": "visor:municipios",
        "visible": True,
        "active": True,
        "attribution": "Visor Urbano México",
        "opacity": 0.7,
        "server_type": "geoserver",
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 0,
        "editable": False,
        "type_geom": "MultiPolygon",
        "cql_filter": None,
        "municipality": [1]
    },
    {
        "id": 3,
        "value": "estados_mexico",
        "label": "Estados México",
        "type": "wms",
        "url": "http://your-geoserver:8080/geoserver/visor/wms",
        "layers": "visor:estados",
        "visible": False,
        "active": True,
        "attribution": "Visor Urbano México",
        "opacity": 0.5,
        "server_type": "geoserver",
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": -1,
        "editable": False,
        "type_geom": "MultiPolygon",
        "cql_filter": "nombre='Chihuahua'",
        "municipality": [1]
    }
]
```

#### Chilean Layers Configuration

```python
# apps/backend/scripts/seed_map_layers.py - Chilean Layers
CHILE_LAYERS_DATA = [
    {
        "id": 10,
        "value": "propiedades_chile",
        "label": "Propiedades Chile",
        "type": "wms",
        "url": "http://your-geoserver:8080/geoserver/visor/wms",
        "layers": "visor:propiedades_chile",
        "visible": True,
        "active": True,
        "attribution": "Visor Urbano Chile",
        "opacity": 1,
        "server_type": "geoserver",
        "projection": "EPSG:32719",
        "version": "1.3.0",
        "format": "image/png",
        "order": 1,
        "editable": True,
        "type_geom": "MultiPolygon",
        "cql_filter": None,
        "municipality": [2]  # Maipú municipality
    },
    {
        "id": 11,
        "value": "comunas_chile",
        "label": "Comunas Chile",
        "type": "wms",
        "url": "http://your-geoserver:8080/geoserver/visor/wms",
        "layers": "visor:comunas",
        "visible": True,
        "active": True,
        "attribution": "Visor Urbano Chile",
        "opacity": 0.7,
        "server_type": "geoserver",
        "projection": "EPSG:32719",
        "version": "1.3.0",
        "format": "image/png",
        "order": 0,
        "editable": False,
        "type_geom": "MultiPolygon",
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 12,
        "value": "regiones_chile",
        "label": "Regiones Chile",
        "type": "wms",
        "url": "http://your-geoserver:8080/geoserver/visor/wms",
        "layers": "visor:regiones",
        "visible": False,
        "active": True,
        "attribution": "Visor Urbano Chile",
        "opacity": 0.5,
        "server_type": "geoserver",
        "projection": "EPSG:32719",
        "version": "1.3.0",
        "format": "image/png",
        "order": -1,
        "editable": False,
        "type_geom": "MultiPolygon",
        "cql_filter": "nombre='Región Metropolitana de Santiago'",
        "municipality": [2]
    },
    {
        "id": 13,
        "value": "calles_maipu",
        "label": "Red Vial Maipú",
        "type": "wms",
        "url": "http://your-geoserver:8080/geoserver/visor/wms",
        "layers": "visor:calles_maipu",
        "visible": False,
        "active": True,
        "attribution": "Municipalidad de Maipú",
        "opacity": 0.8,
        "server_type": "geoserver",
        "projection": "EPSG:32719",
        "version": "1.3.0",
        "format": "image/png",
        "order": 2,
        "editable": False,
        "type_geom": "LineString",
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 14,
        "value": "equipamiento_maipu",
        "label": "Equipamiento Urbano Maipú",
        "type": "wms",
        "url": "http://your-geoserver:8080/geoserver/visor/wms",
        "layers": "visor:equipamiento_maipu",
        "visible": False,
        "active": True,
        "attribution": "Municipalidad de Maipú",
        "opacity": 1,
        "server_type": "geoserver",
        "projection": "EPSG:32719",
        "version": "1.3.0",
        "format": "image/png",
        "order": 3,
        "editable": False,
        "type_geom": "Point",
        "cql_filter": None,
        "municipality": [2]
    }
]

# Combine all layers
LAYERS_DATA = MEXICO_LAYERS_DATA + CHILE_LAYERS_DATA
```

### Step 3: Test Integration

Create a test script to verify the integration:

```python
#!/usr/bin/env python3
"""
Test script to verify GeoServer integration with Visor Urbano
"""

import requests
import json

GEOSERVER_URL = "http://your-geoserver:8080/geoserver"

def test_wms_capabilities():
    """Test WMS GetCapabilities"""
    url = f"{GEOSERVER_URL}/visor/wms"
    params = {
        'service': 'WMS',
        'request': 'GetCapabilities',
        'version': '1.3.0'
    }

    response = requests.get(url, params=params)
    print(f"WMS Capabilities: {response.status_code}")
    return response.status_code == 200

def test_wfs_capabilities():
    """Test WFS GetCapabilities"""
    url = f"{GEOSERVER_URL}/visor/wfs"
    params = {
        'service': 'WFS',
        'request': 'GetCapabilities',
        'version': '2.0.0'
    }

    response = requests.get(url, params=params)
    print(f"WFS Capabilities: {response.status_code}")
    return response.status_code == 200

def test_property_query():
    """Test property query (similar to Visor Urbano)"""
    url = f"{GEOSERVER_URL}/visor/wfs"
    params = {
        'service': 'WFS',
        'request': 'GetFeature',
        'version': '2.0.0',
        'typename': 'visor:predios',
        'count': 1,
        'outputFormat': 'application/json',
        'cql_filter': 'CONTAINS(geom, POINT(-106.0889 28.6353))'
    }

    response = requests.get(url, params=params)
    print(f"Property Query: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Features found: {len(data.get('features', []))}")
        return True
    return False

if __name__ == "__main__":
    print("Testing GeoServer integration...")

    tests = [
        test_wms_capabilities,
        test_wfs_capabilities,
        test_property_query
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test failed: {e}")
            results.append(False)

    if all(results):
        print("✅ All tests passed! GeoServer is ready for Visor Urbano")
    else:
        print("❌ Some tests failed. Check configuration.")
```

---

## Testing & Validation

### Step 1: Test Layer Access

Test each layer individually:

```bash
# Test WMS GetMap for predios
curl "http://localhost:8080/geoserver/visor/wms?service=WMS&version=1.3.0&request=GetMap&layers=visor:predios&styles=&bbox=-106.5,28.2,-105.5,29.2&width=512&height=512&srs=EPSG:4326&format=image/png"

# Test WFS GetFeature for predios
curl "http://localhost:8080/geoserver/visor/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=visor:predios&count=1&outputFormat=application/json"

# Test WMS GetFeatureInfo
curl "http://localhost:8080/geoserver/visor/wms?service=WMS&version=1.3.0&request=GetFeatureInfo&layers=visor:predios&query_layers=visor:predios&styles=&bbox=-106.1,-28.5,-106.0,28.7&width=256&height=256&srs=EPSG:4326&format=image/png&info_format=application/json&i=128&j=128"
```

### Step 2: Performance Testing

Test performance with concurrent requests:

```python
#!/usr/bin/env python3
import concurrent.futures
import requests
import time

def make_request():
    url = "http://localhost:8080/geoserver/visor/wfs"
    params = {
        'service': 'WFS',
        'request': 'GetFeature',
        'version': '2.0.0',
        'typename': 'visor:predios',
        'count': 10,
        'outputFormat': 'application/json'
    }

    start_time = time.time()
    response = requests.get(url, params=params)
    end_time = time.time()

    return response.status_code, end_time - start_time

# Test with 10 concurrent requests
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(make_request) for _ in range(10)]
    results = [future.result() for future in futures]

success_count = sum(1 for status, _ in results if status == 200)
avg_time = sum(duration for _, duration in results) / len(results)

print(f"Successful requests: {success_count}/10")
print(f"Average response time: {avg_time:.2f} seconds")
```

### Step 3: Integration Testing with Visor Urbano

1. Start your Visor Urbano application
2. Navigate to the map route: `http://localhost:3000/map`
3. Verify:
   - Map loads without errors
   - Layers are visible in the layer control
   - Clicking on map shows property information
   - Layer toggle functionality works
   - No CORS errors in browser console

---

## Troubleshooting

### Common Issues and Solutions

#### 1. GeoServer Won't Start

**Problem**: Tomcat/GeoServer fails to start

**Solutions**:

```bash
# Check Java version
java -version

# Check Tomcat logs
sudo tail -f /var/log/tomcat9/catalina.out

# Check memory settings
ps aux | grep tomcat

# Increase memory if needed
sudo systemctl edit tomcat9
[Service]
Environment="JAVA_OPTS=-Xmx2048m -XX:+UseConcMarkSweepGC"
```

#### 2. Database Connection Failed

**Problem**: Cannot connect to PostgreSQL

**Solutions**:

```bash
# Test database connection
psql -h localhost -U gis_user -d visor_urbano

# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection settings in pg_hba.conf
sudo nano /etc/postgresql/12/main/pg_hba.conf

# Verify user permissions
sudo -u postgres psql -c "\du"
```

#### 3. Layers Not Displaying

**Problem**: Layers appear in list but don't render

**Solutions**:

1. Check layer bounding box: **Layers** → **Layer** → **Compute from data**
2. Verify CRS settings: Ensure EPSG:4326 is used consistently
3. Check data integrity:

   ```sql
   -- Check for invalid geometries
   SELECT id, ST_IsValid(geom) FROM predios WHERE NOT ST_IsValid(geom);

   -- Fix invalid geometries
   UPDATE predios SET geom = ST_MakeValid(geom) WHERE NOT ST_IsValid(geom);
   ```

#### 4. CORS Issues

**Problem**: Browser blocks requests due to CORS

**Solutions**:

1. Add CORS headers to web.xml (shown in Security section)
2. Use reverse proxy with proper headers:
   ```nginx
   location /geoserver/ {
       proxy_pass http://localhost:8080/geoserver/;
       add_header Access-Control-Allow-Origin "*";
       add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
       add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range";
   }
   ```

#### 5. Performance Issues

**Problem**: Slow response times

**Solutions**:

1. Add spatial indexes:

   ```sql
   CREATE INDEX CONCURRENTLY idx_predios_geom ON predios USING GIST (geom);
   ```

2. Optimize PostgreSQL:

   ```sql
   -- Analyze tables
   ANALYZE predios;
   ANALYZE municipios;
   ANALYZE estados;

   -- Update statistics
   VACUUM ANALYZE;
   ```

3. Enable GeoServer caching
4. Reduce feature limits for WFS
5. Use CQL filters to limit data

#### 6. WFS Query Issues

**Problem**: CQL filters not working

**Solutions**:

1. Check CQL syntax:

   ```sql
   -- Valid CQL examples
   CONTAINS(geom, POINT(-106.0889 28.6353))
   municipio_id = 1
   NOM_MUN LIKE 'Chihuahua%'
   ```

2. Verify column names in database
3. Check data types (text vs numeric)

### Log Analysis

Important log locations:

```bash
# GeoServer logs
/opt/geoserver/logs/geoserver.log

# Tomcat logs
/var/log/tomcat9/catalina.out
/var/log/tomcat9/localhost.*.log

# PostgreSQL logs
/var/log/postgresql/postgresql-12-main.log
```

### Health Check Script

Create a monitoring script:

```bash
#!/bin/bash
# geoserver-health-check.sh

GEOSERVER_URL="http://localhost:8080/geoserver"

# Check if GeoServer is responding
if curl -f -s "$GEOSERVER_URL" > /dev/null; then
    echo "✅ GeoServer is responding"
else
    echo "❌ GeoServer is not responding"
    exit 1
fi

# Check database connection
if sudo -u postgres psql -d visor_urbano -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Database is accessible"
else
    echo "❌ Database connection failed"
    exit 1
fi

# Check key layers
LAYERS=("visor:predios" "visor:municipios" "visor:estados")

for layer in "${LAYERS[@]}"; do
    if curl -f -s "$GEOSERVER_URL/visor/wfs?service=WFS&request=GetFeature&typename=$layer&count=1" > /dev/null; then
        echo "✅ Layer $layer is accessible"
    else
        echo "❌ Layer $layer failed"
        exit 1
    fi
done

echo "🎉 All health checks passed!"
```

---

## Next Steps

After completing this setup:

1. **Load Real Data**: Replace sample data with actual cadastral information
2. **Configure Additional Layers**: Add zoning, infrastructure, and other municipal layers
3. **Set Up Backup**: Implement regular backups of both GeoServer configuration and PostGIS data
4. **Monitor Performance**: Set up monitoring for GeoServer and database performance
5. **SSL Configuration**: Configure HTTPS for production deployment
6. **Load Balancing**: Consider multiple GeoServer instances for high availability

### Additional Resources

- [GeoServer User Manual](http://docs.geoserver.org/stable/en/user/)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [OpenLayers Documentation](https://openlayers.org/en/latest/doc/)
- [Visor Urbano Documentation](./MAP_ROUTE_DOCUMENTATION.md)

---

This guide provides a complete foundation for setting up GeoServer to work with Visor Urbano. Adjust the configuration based on your specific data and requirements.
