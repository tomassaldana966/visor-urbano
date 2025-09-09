# Production Deployment

Complete guide for deploying Visor Urbano to production environments.

## Deployment Options

### 1. Docker Deployment (Recommended)

#### Prerequisites

- Docker 24.x with Docker Compose
- SSL certificates
- Domain name configured

#### Steps

```bash
# 1. Clone repository
git clone https://github.com/Delivery-Associates/visor-urbano.git
cd visor-urbano

# 2. Configure environment
cp .env.example .env
# Edit .env with production values

# 3. Build and start services
docker-compose -f docker-compose.prod.yml up -d

# 4. Initialize database
docker-compose exec backend alembic upgrade head

# 5. Verify deployment
curl https://your-domain.com/health
```

### 2. Cloud Platform Deployment

#### AWS Deployment

```bash
# Using AWS CLI and ECS
aws ecs create-cluster --cluster-name visor-urbano-prod

# Deploy with CloudFormation
aws cloudformation create-stack \
  --stack-name visor-urbano \
  --template-body file://aws/cloudformation.yml
```

#### Azure Deployment

```bash
# Using Azure CLI
az group create --name visor-urbano-rg --location eastus

# Deploy with ARM template
az deployment group create \
  --resource-group visor-urbano-rg \
  --template-file azure/template.json
```

## Environment Configuration

### Required Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/visor_urbano
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=visor_urbano
DATABASE_USER=visor_user
DATABASE_PASSWORD=secure_password

# Redis
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
SECRET_KEY=your-super-secret-key-here
JWT_SECRET=jwt-secret-key
CORS_ORIGINS=https://your-domain.com

# File Storage
FILE_STORAGE_BUCKET=visor-urbano-files
FILE_STORAGE_REGION=us-east-1

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@domain.com
SMTP_PASSWORD=email-password
```

### SSL/HTTPS Configuration

```nginx
# Nginx configuration
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Database Setup

### PostgreSQL Configuration

```sql
-- Create database and user
CREATE DATABASE visor_urbano;
CREATE USER visor_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE visor_urbano TO visor_user;

-- Enable extensions
\c visor_urbano
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Database Migration

```bash
# Run migrations
cd apps/backend
alembic upgrade head

# Create initial admin user
python scripts/create_admin.py
```

## Performance Optimization

### Application Tuning

```python
# Backend optimization
WORKERS=4
WORKER_CLASS=uvicorn.workers.UvicornWorker
WORKER_CONNECTIONS=1000
MAX_REQUESTS=1000
TIMEOUT=30
```

### Database Optimization

```sql
-- Recommended PostgreSQL settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
random_page_cost = 1.1
```

## Monitoring and Logging

### Application Monitoring

```yaml
# Docker Compose monitoring stack
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - '9090:9090'

  grafana:
    image: grafana/grafana
    ports:
      - '3001:3000'

  app:
    build: .
    environment:
      - PROMETHEUS_METRICS=true
```

### Log Configuration

```python
# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/visor-urbano/app.log',
        },
    },
    'loggers': {
        'visor_urbano': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Security Configuration

### Security Headers

```python
# FastAPI security middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["your-domain.com", "*.your-domain.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Database Security

```bash
# PostgreSQL security
# 1. Enable SSL connections only
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'

# 2. Restrict connections
listen_addresses = 'localhost'
port = 5432

# 3. Configure authentication
# Edit pg_hba.conf
hostssl all all 0.0.0.0/0 md5
```

## Backup and Recovery

### Database Backup

```bash
#!/bin/bash
# Automated backup script
BACKUP_DIR="/backups/visor-urbano"
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump -h localhost -U visor_user visor_urbano > \
  $BACKUP_DIR/visor_urbano_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/visor_urbano_$DATE.sql

# Remove backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

### File Storage Backup

```bash
# Backup uploaded files
aws s3 sync /app/uploads s3://visor-urbano-backups/uploads/

# Backup with versioning
aws s3 cp /app/uploads s3://visor-urbano-backups/uploads/ \
  --recursive --storage-class STANDARD_IA
```

## Health Checks

### Application Health

```python
# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "database": await check_database(),
        "redis": await check_redis(),
    }
```

### Monitoring Setup

```bash
# Using curl for health checks
#!/bin/bash
HEALTH_URL="https://your-domain.com/health"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $STATUS -ne 200 ]; then
    echo "Health check failed with status $STATUS"
    # Send alert notification
fi
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**

   - Check database credentials
   - Verify network connectivity
   - Check PostgreSQL logs

2. **High Memory Usage**

   - Monitor application metrics
   - Check for memory leaks
   - Optimize database queries

3. **Slow Performance**
   - Enable database query logging
   - Check Redis cache hit rates
   - Monitor server resources

### Log Locations

```bash
# Application logs
/var/log/visor-urbano/app.log

# Database logs
/var/log/postgresql/postgresql.log

# Nginx logs
/var/log/nginx/access.log
/var/log/nginx/error.log
```

## Scaling Considerations

### Horizontal Scaling

- Load balancer configuration
- Database read replicas
- Redis clustering
- File storage distribution

### Vertical Scaling

- CPU and memory upgrades
- Database performance tuning
- Storage optimization

## Next Steps

- Review [System Requirements](../getting-started/system-requirements.md)
- Check [API Integration](../development/api-integration.md)
- Monitor application performance
