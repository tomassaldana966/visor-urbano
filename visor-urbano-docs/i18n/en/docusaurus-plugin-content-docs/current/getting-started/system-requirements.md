# 🛠️ System Requirements

This document outlines the complete system requirements for developing, testing, and deploying Visor Urbano across different environments.

## 🎯 Overview

Visor Urbano is a modern full-stack application that requires specific software dependencies and hardware specifications for optimal performance.

### Technology Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python + FastAPI + SQLAlchemy
- **Database**: PostgreSQL + PostGIS
- **Documentation**: Docusaurus + Storybook
- **Testing**: Vitest + Playwright + Pytest

## 💻 Development Environment

### Operating System Support

| OS              | Version       | Status         | Notes                          |
| --------------- | ------------- | -------------- | ------------------------------ |
| **macOS**       | 11+ (Big Sur) | ✅ Recommended | Native development environment |
| **Ubuntu**      | 20.04 LTS+    | ✅ Recommended | Primary CI/CD environment      |
| **Windows**     | 10/11 + WSL2  | ✅ Supported   | Use WSL2 for best experience   |
| **CentOS/RHEL** | 8+            | ✅ Supported   | Enterprise deployment          |
| **Debian**      | 11+           | ✅ Supported   | Alternative Linux option       |

### Hardware Requirements

#### Minimum Development Requirements

| Component   | Minimum    | Recommended | Notes                    |
| ----------- | ---------- | ----------- | ------------------------ |
| **CPU**     | 4 cores    | 8+ cores    | M1/M2 Mac or Intel i5+   |
| **RAM**     | 8 GB       | 16+ GB      | 32 GB for large datasets |
| **Storage** | 50 GB free | 200+ GB SSD | NVMe SSD recommended     |
| **Network** | Broadband  | High-speed  | For map tile downloads   |

#### Performance Considerations

- **SSD highly recommended** for database performance
- **16+ GB RAM** when working with large GIS datasets
- **Dedicated GPU** beneficial for complex map rendering
- **Multiple monitors** helpful for development workflow

## 🛠️ Software Dependencies

### Core Development Tools

#### Node.js and Package Management

```bash
# Node.js (Required: v18+)
node --version  # Should be 18.0.0 or higher

# pnpm (Required: v8+)
npm install -g pnpm
pnpm --version  # Should be 8.0.0 or higher

# Alternative: npm (if pnpm not available)
npm --version  # Should be 9.0.0 or higher
```

#### Python Environment

```bash
# Python (Required: v3.9+)
python --version  # Should be 3.9.0 or higher
python3 --version # On systems with multiple Python versions

# pip (Package installer)
pip --version

# Virtual environment support
python -m venv --help
```

#### Database System

```bash
# PostgreSQL (Required: v13+)
psql --version  # Should be 13.0 or higher

# PostGIS (Required: v3.1+)
# Check in PostgreSQL:
# SELECT PostGIS_Version();
```

#### Version Control

```bash
# Git (Required: v2.30+)
git --version

# Git LFS (for large files)
git lfs version
```

### Development Tools

#### Code Editors (Choose one)

| Editor             | Configuration    | Extensions                           |
| ------------------ | ---------------- | ------------------------------------ |
| **VS Code**        | Recommended      | ESLint, Prettier, Python, TypeScript |
| **JetBrains IDEs** | WebStorm/PyCharm | Built-in support                     |
| **Vim/Neovim**     | Advanced users   | Language server setup required       |

#### Browser Requirements

| Browser     | Version | DevTools | Notes                       |
| ----------- | ------- | -------- | --------------------------- |
| **Chrome**  | 90+     | ✅       | Primary development browser |
| **Firefox** | 85+     | ✅       | Secondary testing           |
| **Safari**  | 14+     | ✅       | macOS testing               |
| **Edge**    | 90+     | ✅       | Windows testing             |

### Optional Development Tools

```bash
# Docker (for containerized development)
docker --version
docker-compose --version

# Make (for automation scripts)
make --version

# curl (for API testing)
curl --version

# jq (for JSON processing)
jq --version
```

## 🗄️ Database Requirements

### PostgreSQL Installation

#### Ubuntu/Debian

```bash
# Install PostgreSQL and PostGIS
sudo apt update
sudo apt install postgresql-13 postgresql-13-postgis-3
sudo apt install postgresql-client-13 postgis

# Start and enable service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### macOS (Homebrew)

```bash
# Install PostgreSQL
brew install postgresql@13 postgis

# Start service
brew services start postgresql@13
```

#### Windows

```bash
# Download from postgresql.org
# Or use chocolatey
choco install postgresql13 --params '/Password:yourpassword'
```

### Database Configuration

#### Required Extensions

```sql
-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;
```

#### Performance Settings

```sql
-- Recommended PostgreSQL settings for development
-- Add to postgresql.conf

# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB

# Connection settings
max_connections = 100

# Logging (for development)
log_statement = 'all'
log_duration = on
```

### Database Size Estimates

| Data Type       | Small City | Medium City | Large City |
| --------------- | ---------- | ----------- | ---------- |
| **Base Schema** | 50 MB      | 50 MB       | 50 MB      |
| **GIS Layers**  | 500 MB     | 2 GB        | 10 GB      |
| **Permit Data** | 100 MB     | 1 GB        | 5 GB       |
| **Documents**   | 1 GB       | 10 GB       | 50 GB      |
| **Total**       | ~2 GB      | ~15 GB      | ~70 GB     |

## 🌐 Network Requirements

### Development

| Service       | Port | Protocol | Purpose           |
| ------------- | ---- | -------- | ----------------- |
| Frontend      | 5173 | HTTP     | React dev server  |
| Backend       | 8000 | HTTP     | FastAPI server    |
| Database      | 5432 | TCP      | PostgreSQL        |
| Storybook     | 6006 | HTTP     | Component library |
| Documentation | 3000 | HTTP     | Docusaurus        |

### External Dependencies

```bash
# Test external connectivity
curl -I https://api.mapbox.com  # Map tiles
curl -I https://nominatim.openstreetmap.org  # Geocoding
curl -I https://registry.npmjs.org  # npm packages
curl -I https://pypi.org  # Python packages
```

### Bandwidth Requirements

| Activity        | Bandwidth | Notes                 |
| --------------- | --------- | --------------------- |
| **Development** | 10+ Mbps  | For package downloads |
| **Map Loading** | 5+ Mbps   | For tile servers      |
| **Production**  | 100+ Mbps | For user traffic      |

## 🧪 Testing Environment

### Additional Testing Tools

```bash
# Frontend testing
npm install -g @playwright/test

# API testing
pip install pytest pytest-asyncio httpx

# Load testing
npm install -g autocannon
pip install locust
```

### Browser Testing Matrix

| Browser | Desktop | Mobile | Testing Priority |
| ------- | ------- | ------ | ---------------- |
| Chrome  | ✅      | ✅     | Primary          |
| Firefox | ✅      | ✅     | Secondary        |
| Safari  | ✅      | ✅     | macOS/iOS        |
| Edge    | ✅      | ❌     | Windows          |

## 🚀 Production Environment

### Server Requirements

#### Minimum Production Server

| Component   | Specification    |
| ----------- | ---------------- |
| **CPU**     | 4 cores, 2.4 GHz |
| **RAM**     | 16 GB            |
| **Storage** | 200 GB SSD       |
| **Network** | 100 Mbps         |
| **OS**      | Ubuntu 20.04 LTS |

#### Recommended Production Server

| Component   | Specification     |
| ----------- | ----------------- |
| **CPU**     | 8+ cores, 3.0 GHz |
| **RAM**     | 32+ GB            |
| **Storage** | 500+ GB NVMe SSD  |
| **Network** | 1+ Gbps           |
| **OS**      | Ubuntu 22.04 LTS  |

### Production Software Stack

```bash
# Web server
nginx --version  # v1.18+

# Process manager
systemctl --version  # systemd

# Container runtime (optional)
docker --version  # v20.10+

# Monitoring
# Prometheus, Grafana, etc.
```

### Security Requirements

| Component      | Requirement | Implementation                            |
| -------------- | ----------- | ----------------------------------------- |
| **SSL/TLS**    | Required    | Let's Encrypt or commercial cert          |
| **Firewall**   | Required    | UFW, iptables, or cloud security groups   |
| **Backups**    | Required    | Automated daily backups                   |
| **Monitoring** | Required    | Application and infrastructure monitoring |

## 🔧 Development Setup Verification

### Quick Verification Script

```bash
#!/bin/bash
# verify-setup.sh

echo "🔍 Verifying Visor Urbano development setup..."

# Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
else
    echo "❌ Node.js not found"
fi

# pnpm
if command -v pnpm &> /dev/null; then
    PNPM_VERSION=$(pnpm --version)
    echo "✅ pnpm: $PNPM_VERSION"
else
    echo "⚠️  pnpm not found (npm available as alternative)"
fi

# Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found"
fi

# PostgreSQL
if command -v psql &> /dev/null; then
    PSQL_VERSION=$(psql --version)
    echo "✅ PostgreSQL: $PSQL_VERSION"
else
    echo "❌ PostgreSQL not found"
fi

# Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "✅ Git: $GIT_VERSION"
else
    echo "❌ Git not found"
fi

echo "✨ Setup verification complete!"
```

### Performance Benchmarks

#### Expected Development Performance

| Metric          | Target | Acceptable |
| --------------- | ------ | ---------- |
| **App startup** | < 30s  | < 60s      |
| **Hot reload**  | < 2s   | < 5s       |
| **Test suite**  | < 60s  | < 120s     |
| **Build time**  | < 2min | < 5min     |

#### Database Performance

```sql
-- Test spatial query performance
EXPLAIN ANALYZE
SELECT COUNT(*)
FROM permits
WHERE ST_Intersects(
    geometry,
    ST_Buffer(ST_Point(-70.6693, -33.4489), 0.01)
);

-- Should complete in < 100ms with proper indexes
```

## 🐛 Troubleshooting Common Issues

### Node.js Version Issues

```bash
# Install Node Version Manager
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install and use Node.js 18
nvm install 18
nvm use 18
```

### Python Virtual Environment

```bash
# Create isolated Python environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install requirements
pip install -r requirements.txt
```

### PostgreSQL Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Reset password if needed
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'newpassword';"

# Test connection
psql -U postgres -h localhost -d postgres
```

### Port Conflicts

```bash
# Find process using port
lsof -i :5173
netstat -tulpn | grep :5173

# Kill process
kill -9 <process-id>
```

## 📚 Platform-Specific Notes

### macOS Development

- Use Homebrew for package management
- Install Xcode Command Line Tools
- Consider using Docker Desktop for containers
- PostgreSQL.app as alternative to Homebrew

### Windows Development

- Use WSL2 for Linux compatibility
- Install Windows Terminal for better CLI experience
- Use PostgreSQL Windows installer
- Consider VS Code with Remote-WSL extension

### Linux Development

- Use system package manager (apt, yum, etc.)
- Consider using Docker for isolation
- Ensure proper user permissions for PostgreSQL
- Use systemd for service management

## 🔗 Related Documentation

- [Quick Setup Guide](./quick-setup.md) - Get started quickly
- [Setup Integration](../development/setup-integration.md) - Advanced configuration
- [Production Deployment](../deployment/production-deployment.md) - Production requirements

---

This system requirements document ensures you have everything needed for successful Visor Urbano development. Update your system according to these specifications before proceeding with the [Quick Setup Guide](./quick-setup.md).
