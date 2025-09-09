# 🚀 Production Deployment

This comprehensive guide covers the deployment of Visor Urbano to production environments, including infrastructure setup, security considerations, monitoring, and maintenance procedures.

## 🎯 Deployment Overview

Visor Urbano production deployment supports multiple infrastructure approaches:

- **Cloud Deployment**: AWS, Azure, Google Cloud Platform
- **On-Premises**: Traditional server infrastructure
- **Hybrid**: Combination of cloud and on-premises
- **Container Orchestration**: Kubernetes, Docker Swarm

## 🏗️ Infrastructure Requirements

### Minimum Production Requirements

#### Hardware Specifications

| Component   | Minimum    | Recommended      |
| ----------- | ---------- | ---------------- |
| **CPU**     | 4 cores    | 8+ cores         |
| **RAM**     | 16 GB      | 32+ GB           |
| **Storage** | 100 GB SSD | 500+ GB NVMe SSD |
| **Network** | 100 Mbps   | 1 Gbps           |

#### Software Requirements

- **Operating System**: Ubuntu 20.04 LTS or CentOS 8+
- **Database**: PostgreSQL 13+ with PostGIS 3.1+
- **Web Server**: Nginx 1.18+ or Apache 2.4+
- **Container Runtime**: Docker 20.10+ (if using containers)
- **SSL Certificate**: Valid TLS certificate for HTTPS

### Scalability Planning

#### Small Municipality (< 50,000 inhabitants)

```yaml
configuration:
  frontend_instances: 2
  backend_instances: 2
  database: single_instance
  storage: 200GB
  concurrent_users: 100
```

#### Medium Municipality (50,000 - 200,000 inhabitants)

```yaml
configuration:
  frontend_instances: 3
  backend_instances: 4
  database: primary_replica_setup
  storage: 500GB
  concurrent_users: 500
```

#### Large Municipality (> 200,000 inhabitants)

```yaml
configuration:
  frontend_instances: 5+
  backend_instances: 8+
  database: clustered_setup
  storage: 1TB+
  concurrent_users: 1000+
```

## 🐳 Container Deployment

### Docker Production Setup

#### 1. Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - frontend
      - backend

  frontend:
    build:
      context: ./apps/frontend
      dockerfile: Dockerfile.prod
    environment:
      - VITE_API_URL=https://api.yourdomain.com
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure

  backend:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile.prod
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/visor_urbano
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    deploy:
      replicas: 4
      restart_policy:
        condition: on-failure

  db:
    image: postgis/postgis:13-3.1
    environment:
      - POSTGRES_DB=visor_urbano
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    deploy:
      restart_policy:
        condition: on-failure

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    deploy:
      restart_policy:
        condition: on-failure

volumes:
  postgres_data:
  redis_data:
```

#### 2. Production Dockerfile (Backend)

```dockerfile
# apps/backend/Dockerfile.prod
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 3. Production Dockerfile (Frontend)

```dockerfile
# apps/frontend/Dockerfile.prod
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80 || exit 1

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## ☸️ Kubernetes Deployment

### Kubernetes Manifests

#### 1. Namespace

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: visor-urbano
```

#### 2. ConfigMap

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: visor-urbano-config
  namespace: visor-urbano
data:
  DATABASE_HOST: 'postgres-service'
  DATABASE_PORT: '5432'
  DATABASE_NAME: 'visor_urbano'
  REDIS_HOST: 'redis-service'
  REDIS_PORT: '6379'
```

#### 3. Secrets

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: visor-urbano-secrets
  namespace: visor-urbano
type: Opaque
data:
  database-password: <base64-encoded-password>
  secret-key: <base64-encoded-secret>
```

#### 4. Backend Deployment

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: visor-urbano
spec:
  replicas: 4
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: visor-urbano/backend:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              value: 'postgresql://$(DATABASE_USER):$(DATABASE_PASSWORD)@$(DATABASE_HOST):$(DATABASE_PORT)/$(DATABASE_NAME)'
          envFrom:
            - configMapRef:
                name: visor-urbano-config
            - secretRef:
                name: visor-urbano-secrets
          resources:
            requests:
              memory: '512Mi'
              cpu: '250m'
            limits:
              memory: '1Gi'
              cpu: '500m'
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
```

#### 5. Service and Ingress

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: visor-urbano
spec:
  selector:
    app: backend
  ports:
    - port: 8000
      targetPort: 8000
  type: ClusterIP

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: visor-urbano-ingress
  namespace: visor-urbano
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - visor-urbano.yourdomain.com
      secretName: visor-urbano-tls
  rules:
    - host: visor-urbano.yourdomain.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: backend-service
                port:
                  number: 8000
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
```

## 🔧 Web Server Configuration

### Nginx Configuration

```nginx
# nginx.conf
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:80;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL configuration
    ssl_certificate /etc/ssl/certs/yourdomain.com.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # API routes
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Body size for file uploads
        client_max_body_size 50M;
    }

    # Frontend routes
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    gzip_min_length 1000;
}
```

## 🔒 Security Configuration

### Environment Variables

```bash
# production.env
# Database
DATABASE_URL=postgresql://user:password@db-host:5432/visor_urbano
DATABASE_URL_TEST=postgresql://user:password@db-host:5432/visor_urbano_test

# Security
SECRET_KEY=your-super-secure-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256

# CORS
ALLOWED_ORIGINS=["https://yourdomain.com"]

# File uploads
UPLOAD_FOLDER=/app/uploads
MAX_FILE_SIZE=52428800  # 50MB

# Email
SMTP_HOST=smtp.yourdomain.com
SMTP_PORT=587
SMTP_USERNAME=noreply@yourdomain.com
SMTP_PASSWORD=email-password

# External services
MAPBOX_TOKEN=your-mapbox-token
SENTRY_DSN=your-sentry-dsn

# Monitoring
PROMETHEUS_METRICS=true
LOG_LEVEL=INFO
```

### SSL/TLS Configuration

#### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal cron job
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

#### Manual Certificate Installation

```bash
# Create SSL directory
sudo mkdir -p /etc/ssl/certs /etc/ssl/private

# Copy certificates
sudo cp yourdomain.com.crt /etc/ssl/certs/
sudo cp yourdomain.com.key /etc/ssl/private/

# Set permissions
sudo chmod 644 /etc/ssl/certs/yourdomain.com.crt
sudo chmod 600 /etc/ssl/private/yourdomain.com.key
```

## 📊 Monitoring and Logging

### Application Monitoring

#### Prometheus + Grafana Setup

```yaml
# monitoring/docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - '9090:9090'
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana
    ports:
      - '3001:3000'
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

  node-exporter:
    image: prom/node-exporter
    ports:
      - '9100:9100'

volumes:
  prometheus_data:
  grafana_data:
```

#### Health Check Endpoints

```python
# Backend health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "database": await check_database_connection(),
        "redis": await check_redis_connection()
    }

@app.get("/metrics")
async def metrics():
    # Prometheus metrics endpoint
    return Response(
        generate_latest(),
        media_type="text/plain"
    )
```

### Logging Configuration

#### Structured Logging (JSON)

```python
# logging_config.py
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "/var/log/visor-urbano/app.log",
            "formatter": "json",
            "level": "INFO"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
}
```

#### Log Aggregation with ELK Stack

```yaml
# elk/docker-compose.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
      - 'ES_JAVA_OPTS=-Xms512m -Xmx512m'
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:7.14.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
    ports:
      - '5601:5601'
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

## 💾 Database Management

### Production Database Setup

```bash
# PostgreSQL + PostGIS installation
sudo apt-get install postgresql-13 postgresql-13-postgis-3

# Create database and user
sudo -u postgres createuser visor_urbano
sudo -u postgres createdb visor_urbano -O visor_urbano
sudo -u postgres psql -c "ALTER USER visor_urbano PASSWORD 'secure_password';"

# Enable PostGIS
sudo -u postgres psql visor_urbano -c "CREATE EXTENSION postgis;"
sudo -u postgres psql visor_urbano -c "CREATE EXTENSION postgis_topology;"
```

### Database Backup Strategy

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="visor_urbano"

# Create backup
pg_dump -Fc $DB_NAME > $BACKUP_DIR/visor_urbano_$DATE.dump

# Rotate backups (keep last 7 days)
find $BACKUP_DIR -name "visor_urbano_*.dump" -mtime +7 -delete

# Upload to cloud storage (optional)
aws s3 cp $BACKUP_DIR/visor_urbano_$DATE.dump s3://your-backup-bucket/
```

### Database Performance Tuning

```sql
-- PostgreSQL configuration for production
-- /etc/postgresql/13/main/postgresql.conf

-- Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

-- Checkpoint settings
checkpoint_completion_target = 0.9
wal_buffers = 16MB

-- Connection settings
max_connections = 200

-- Logging
log_statement = 'mod'
log_duration = on
log_min_duration_statement = 1000

-- Create indexes for performance
CREATE INDEX CONCURRENTLY idx_permits_geom ON permits USING GIST(geometry);
CREATE INDEX CONCURRENTLY idx_permits_status ON permits(status);
CREATE INDEX CONCURRENTLY idx_permits_created_at ON permits(created_at);
```

## 🔄 CI/CD Pipeline

### GitHub Actions Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker images
        run: |
          docker build -t visor-urbano/frontend:${{ github.sha }} ./apps/frontend
          docker build -t visor-urbano/backend:${{ github.sha }} ./apps/backend

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push visor-urbano/frontend:${{ github.sha }}
          docker push visor-urbano/backend:${{ github.sha }}

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/frontend frontend=visor-urbano/frontend:${{ github.sha }}
          kubectl set image deployment/backend backend=visor-urbano/backend:${{ github.sha }}
          kubectl rollout status deployment/frontend
          kubectl rollout status deployment/backend
```

## 📋 Deployment Checklist

### Pre-Deployment

- [ ] Infrastructure provisioning complete
- [ ] SSL certificates obtained and installed
- [ ] Database setup and migrations applied
- [ ] Environment variables configured
- [ ] DNS records configured
- [ ] Backup procedures implemented
- [ ] Monitoring and alerting setup

### Deployment

- [ ] Application containers built and tested
- [ ] Database backed up
- [ ] Blue-green deployment prepared (if applicable)
- [ ] Load balancer configuration updated
- [ ] Health checks passing
- [ ] Performance testing completed

### Post-Deployment

- [ ] Application functionality verified
- [ ] Performance monitoring active
- [ ] Error tracking configured
- [ ] User acceptance testing completed
- [ ] Documentation updated
- [ ] Support team notified

## 🚨 Disaster Recovery

### Backup Strategy

1. **Database Backups**

   - Daily full backups
   - Hourly incremental backups
   - Cross-region replication

2. **Application Backups**

   - Container images stored in registry
   - Configuration files versioned
   - Static assets backed up

3. **Recovery Procedures**
   - RTO (Recovery Time Objective): 4 hours
   - RPO (Recovery Point Objective): 1 hour
   - Automated failover procedures

### Incident Response

```bash
# Emergency procedures
# 1. Check system status
kubectl get pods -n visor-urbano

# 2. Scale up if needed
kubectl scale deployment backend --replicas=10

# 3. Check logs
kubectl logs -f deployment/backend

# 4. Rollback if necessary
kubectl rollout undo deployment/backend
```

## 🔗 Related Documentation

- [System Requirements](../getting-started/system-requirements.md) - Infrastructure requirements
- [API Integration](../development/api-integration.md) - Application integration details
- [Development Setup](../development/setup-integration.md) - Development environment

---

This production deployment guide provides a comprehensive foundation for deploying Visor Urbano in production environments. Adapt the configurations based on your specific infrastructure requirements and organizational policies.
