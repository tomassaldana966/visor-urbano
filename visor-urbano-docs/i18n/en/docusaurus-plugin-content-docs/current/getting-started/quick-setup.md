# ⚡ Quick Setup Guide

Get Visor Urbano up and running in your development environment in just a few minutes with this streamlined setup guide.

## 🎯 Prerequisites Check

Before starting, ensure you have these tools installed:

```bash
# Check Node.js (v18+)
node --version

# Check pnpm (v8+)
pnpm --version

# Check Python (v3.9+)
python --version

# Check PostgreSQL (v13+)
psql --version

# Check Git
git --version
```

## 🚀 One-Command Setup

For the fastest setup, use our automated script:

```bash
# Clone and setup everything
git clone <repository-url>
cd visor-urbano
chmod +x setup.sh
./setup.sh
```

The setup script will:

1. Install all dependencies
2. Setup environment files
3. Create and configure databases
4. Run initial migrations
5. Start all development services

## 📋 Manual Setup (Step by Step)

### 1. Clone Repository

```bash
git clone <repository-url>
cd visor-urbano
```

### 2. Install Dependencies

```bash
# Install all workspace dependencies
pnpm install
```

### 3. Environment Configuration

```bash
# Copy environment templates
cp apps/backend/.env.example apps/backend/.env
cp apps/frontend/.env.example apps/frontend/.env

# Edit the files with your configuration
nano apps/backend/.env
nano apps/frontend/.env
```

#### Essential Environment Variables

**Backend (.env)**:

```env
DATABASE_URL=postgresql://username:password@localhost/visor_urbano
SECRET_KEY=your-secret-key-here
```

**Frontend (.env)**:

```env
VITE_API_URL=http://localhost:8000
```

### 4. Database Setup

```bash
# Create databases
createdb visor_urbano
createdb visor_urbano_test

# Enable PostGIS extension
psql visor_urbano -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql visor_urbano_test -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Run migrations
cd apps/backend
python -m alembic upgrade head
```

### 5. Start Development Services

```bash
# Start all services (from project root)
pnpm dev
```

This starts:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Storybook**: http://localhost:6006
- **Documentation**: http://localhost:3000

## 🔍 Verify Installation

### Test Frontend

1. Open http://localhost:5173
2. You should see the Visor Urbano homepage
3. Try navigating through different sections

### Test Backend API

```bash
# Test API health
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "timestamp": "..."}
```

### Test Database Connection

```bash
# Test database
psql visor_urbano -c "SELECT version();"

# Test PostGIS
psql visor_urbano -c "SELECT PostGIS_Version();"
```

## 🛠️ Development Tools Access

Once everything is running, access these development tools:

| Tool              | URL                         | Purpose                       |
| ----------------- | --------------------------- | ----------------------------- |
| **Main App**      | http://localhost:5173       | Frontend application          |
| **API Docs**      | http://localhost:8000/docs  | Swagger API documentation     |
| **Storybook**     | http://localhost:6006       | UI component library          |
| **Documentation** | http://localhost:3000       | This technical documentation  |
| **ReDoc**         | http://localhost:8000/redoc | Alternative API documentation |

## 🎨 First Steps After Setup

### 1. Explore the Interface

- Browse the main application at http://localhost:5173
- Check the different sections and features
- Try the map interface and permit workflows

### 2. Review API Documentation

- Visit http://localhost:8000/docs
- Explore available endpoints
- Try the "Try it out" feature for testing

### 3. Check Component Library

- Open http://localhost:6006
- Browse available UI components
- See how components are used and configured

### 4. Understand the Architecture

- Review the [API Integration documentation](../development/api-integration.md)
- Check the project structure
- Understand how frontend and backend connect

## 🔧 Common Setup Issues

### Database Connection Failed

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if needed
sudo systemctl start postgresql

# Check connection settings in .env file
```

### Port Already in Use

```bash
# Check what's using port 5173
lsof -i :5173

# Kill process if needed
kill -9 <process-id>

# Or change port in vite.config.ts
```

### Missing Dependencies

```bash
# Clear and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install

# For backend dependencies
cd apps/backend
pip install -r requirements.txt
```

### PostGIS Extension Error

```bash
# Install PostGIS if missing
sudo apt-get install postgresql-13-postgis-3

# Enable extension
psql visor_urbano -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

## 🚀 Next Steps

### For Frontend Development

1. **Component Development**

   - Start with Storybook at http://localhost:6006
   - Create new components in `packages/ui/components`
   - Follow existing patterns and design system

2. **Route Development**
   - Review existing routes in `apps/frontend/app/routes.ts`
   - Check the [API Integration table](../development/api-integration.md)
   - Follow established patterns for new routes

### For Backend Development

1. **API Development**

   - Check existing endpoints at http://localhost:8000/docs
   - Follow FastAPI patterns in `apps/backend/app`
   - Write tests for new endpoints

2. **Database Models**
   - Review existing models in `apps/backend/app/models`
   - Create migrations for schema changes
   - Test spatial queries in PostgreSQL

### For Full-Stack Features

1. **Study Integration Patterns**

   - Review the [API Integration documentation](../development/api-integration.md)
   - Understand how routes connect to components and endpoints
   - Follow established authentication patterns

2. **Testing**
   - Write unit tests for components and functions
   - Add integration tests for API endpoints
   - Test with real spatial data

## 📚 Essential Documentation

After setup, explore these key documentation sections:

- **[System Requirements](./system-requirements.md)** - Detailed requirements and dependencies
- **[API Integration](../development/api-integration.md)** - Complete frontend-backend mapping
- **[Development Guide](../development/README.md)** - Comprehensive development documentation
- **[Setup Integration](../development/setup-integration.md)** - Advanced configuration options

## 💡 Development Tips

### Efficient Workflow

```bash
# Watch for changes in all services
pnpm dev

# Run tests automatically
pnpm test --watch

# Type checking in watch mode
pnpm type-check --watch
```

### Debugging

```bash
# Check logs for specific services
pnpm logs:frontend
pnpm logs:backend

# Debug with browser dev tools
# Check Network tab for API calls
# Use React Dev Tools for component inspection
```

### Performance

```bash
# Build for testing production performance
pnpm build

# Analyze bundle size
pnpm analyze

# Run performance tests
pnpm test:performance
```

## 🎉 You're Ready!

Congratulations! You now have a fully functional Visor Urbano development environment.

Start exploring the codebase, try making small changes, and refer to the comprehensive [development documentation](../development/README.md) as you build new features.

Happy coding! 🚀
