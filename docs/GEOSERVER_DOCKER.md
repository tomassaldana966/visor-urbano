# 🐳 Running GeoServer with Docker (`kartoza/geoserver`)

This guide explains the system requirements, configuration options, and behavior of the Docker command:

```bash
docker run -d -p 8080:8080 --name=geoserver -e GEOSERVER_ADMIN_USER=admin  -e GEOSERVER_ADMIN_PASSWORD=geoserver  kartoza/geoserver
```

## ✅ Prerequisites

### 1. Docker Installed

Ensure Docker Desktop is installed on your computer. You can download it from:
👉 https://www.docker.com/products/docker-desktop/

Verify installation:

```bash
docker --version
```

### 2. Recommended Docker Resource Allocation

Configure Docker Desktop with at least:

- **2 CPUs**
- **4 GB RAM**
- **4 GB Free Disk Space**

You can adjust this in:
**Docker Desktop → Settings → Resources**

## 🛠️ Image Details (`kartoza/geoserver`)

| Feature               | Value                                  |
| --------------------- | -------------------------------------- |
| Base Image            | Ubuntu + Java JRE + Tomcat + GeoServer |
| Exposed Port          | 8080 (default HTTP)                    |
| GeoServer Version     | Latest stable (e.g., 2.27.1)           |
| Persistent Volumes    | Not configured by default              |
| Env Variables Support | Optional configuration supported       |

## 🌐 Accessing GeoServer

Once the container is running, open:

```
http://localhost:8080/geoserver
```

### Default Credentials

- **Username**: `admin`
- **Password**: `geoserver`

## 📦 Optional: Enable Data Persistence

To persist GeoServer data (e.g., layers, styles, configs):

```bash
docker run -d -p 8080:8080 \
  -v geoserver_data:/opt/geoserver/data_dir \
  --name=geoserver kartoza/geoserver
```

This mounts a Docker volume called `geoserver_data`.

## 🔄 Container Management

```bash
docker stop geoserver         # Stop container
docker start geoserver        # Start again
docker rm -f geoserver        # Remove permanently
```

## ⚙️ Advanced Configuration

### Environment Variables

The `kartoza/geoserver` image supports various environment variables for customization:

```bash
docker run -d -p 8080:8080 \
  -e GEOSERVER_ADMIN_PASSWORD=your_secure_password \
  -e GEOSERVER_ADMIN_USER=admin \
  -e INITIAL_MEMORY=2G \
  -e MAXIMUM_MEMORY=4G \
  -v geoserver_data:/opt/geoserver/data_dir \
  --name=geoserver kartoza/geoserver
```

### Common Environment Variables

| Variable                   | Default     | Description                                  |
| -------------------------- | ----------- | -------------------------------------------- |
| `GEOSERVER_ADMIN_USER`     | `admin`     | Admin username                               |
| `GEOSERVER_ADMIN_PASSWORD` | `geoserver` | Admin password                               |
| `INITIAL_MEMORY`           | `2G`        | Initial JVM memory                           |
| `MAXIMUM_MEMORY`           | `4G`        | Maximum JVM memory                           |
| `STABLE_EXTENSIONS`        | -           | Comma-separated list of extensions           |
| `COMMUNITY_EXTENSIONS`     | -           | Comma-separated list of community extensions |

## 🐳 Docker Compose Configuration

Create a `docker-compose.yml` file for easier management:

```yaml
version: '3.8'

services:
  geoserver:
    image: kartoza/geoserver:latest
    container_name: geoserver
    ports:
      - '8080:8080'
    environment:
      - GEOSERVER_ADMIN_PASSWORD=secure_password_123
      - INITIAL_MEMORY=2G
      - MAXIMUM_MEMORY=4G
    volumes:
      - geoserver_data:/opt/geoserver/data_dir
    restart: unless-stopped
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/geoserver/web/']
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  geoserver_data:
    driver: local
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f geoserver

# Restart services
docker-compose restart
```

## 🔗 Integration with PostgreSQL/PostGIS

To connect GeoServer with a PostgreSQL database, create a complete setup:

```yaml
version: '3.8'

services:
  postgres:
    image: postgis/postgis:15-3.3
    container_name: postgres-gis
    environment:
      - POSTGRES_DB=visor_urbano
      - POSTGRES_USER=geouser
      - POSTGRES_PASSWORD=geopass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - '5432:5432'
    restart: unless-stopped

  geoserver:
    image: kartoza/geoserver:latest
    container_name: geoserver
    depends_on:
      - postgres
    ports:
      - '8080:8080'
    environment:
      - GEOSERVER_ADMIN_PASSWORD=secure_password_123
      - INITIAL_MEMORY=2G
      - MAXIMUM_MEMORY=4G
    volumes:
      - geoserver_data:/opt/geoserver/data_dir
    restart: unless-stopped
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/geoserver/web/']
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  postgres_data:
    driver: local
  geoserver_data:
    driver: local

networks:
  default:
    name: visor-urbano-network
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Container Won't Start

```bash
# Check container logs
docker logs geoserver

# Check if port is already in use
lsof -i :8080
```

#### 2. Out of Memory Errors

```bash
# Increase memory allocation
docker run -d -p 8080:8080 \
  -e INITIAL_MEMORY=4G \
  -e MAXIMUM_MEMORY=8G \
  --name=geoserver kartoza/geoserver
```

#### 3. Data Not Persisting

```bash
# Verify volume is mounted
docker inspect geoserver | grep Mounts -A 10

# Check volume exists
docker volume ls
```

#### 4. Can't Access Web Interface

```bash
# Verify container is running
docker ps

# Check port mapping
docker port geoserver

# Test connectivity
curl -I http://localhost:8080/geoserver
```

### Performance Tuning

#### For Production Use

```bash
docker run -d -p 8080:8080 \
  -e INITIAL_MEMORY=4G \
  -e MAXIMUM_MEMORY=8G \
  -e STABLE_EXTENSIONS="wps,csw,inspire" \
  -v geoserver_data:/opt/geoserver/data_dir \
  --restart=unless-stopped \
  --name=geoserver kartoza/geoserver
```

## 🔐 Security Considerations

### 1. Change Default Password

Always change the default admin password:

```bash
docker run -d -p 8080:8080 \
  -e GEOSERVER_ADMIN_PASSWORD=your_very_secure_password \
  --name=geoserver kartoza/geoserver
```

### 2. Network Security

For production, consider:

- Using reverse proxy (nginx/Apache)
- Enabling HTTPS
- Restricting network access
- Using Docker secrets for passwords

### 3. Backup Strategy

```bash
# Backup GeoServer data
docker run --rm -v geoserver_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/geoserver-backup-$(date +%Y%m%d).tar.gz /data

# Restore GeoServer data
docker run --rm -v geoserver_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/geoserver-backup-YYYYMMDD.tar.gz -C /
```

## 📚 Additional Resources

- [Kartoza GeoServer Docker Documentation](https://github.com/kartoza/docker-geoserver)
- [GeoServer Official Documentation](http://docs.geoserver.org/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Visor Urbano Main Setup Guide](./GEOSERVER_SETUP_GUIDE_EN.md)
