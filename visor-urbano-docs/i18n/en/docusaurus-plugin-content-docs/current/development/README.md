# 👨‍💻 Development Guide

Welcome to the Visor Urbano development documentation. This section contains comprehensive guides for developers contributing to the project.

## 🚀 Quick Start

If you're new to the project, start here:

1. **[System Requirements](../getting-started/system-requirements.md)** - Prerequisites and setup
2. **[Quick Setup](../getting-started/quick-setup.md)** - Get up and running quickly
3. **[API Integration](./api-integration.md)** - Understanding the complete stack integration

## 📚 Development Documentation

### Core Development

- **[API Integration](./api-integration.md)** - Route-Component-Endpoint mapping
- **[API Documentation](./api-documentation.md)** - Backend API reference
- **[Setup Integration](./setup-integration.md)** - Configuration and development environment

### Architecture

Our development follows a modern full-stack architecture:

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python + FastAPI + SQLAlchemy
- **Database**: PostgreSQL with PostGIS for geospatial data
- **Documentation**: Storybook + Swagger + Docusaurus
- **Testing**: Vitest + Playwright + Pytest

## 🛠️ Development Tools

| Tool             | Purpose                  | URL                           |
| ---------------- | ------------------------ | ----------------------------- |
| **Storybook**    | UI Component Development | `http://localhost:6006`       |
| **Swagger UI**   | API Documentation        | `http://localhost:8000/docs`  |
| **ReDoc**        | Alternative API View     | `http://localhost:8000/redoc` |
| **Docusaurus**   | Technical Documentation  | `http://localhost:3000`       |
| **Frontend Dev** | React Application        | `http://localhost:5173`       |

## 🏗️ Project Structure

```
visor-urbano/
├── apps/
│   ├── frontend/        # React TypeScript application
│   ├── backend/         # Python FastAPI server
│   └── e2e/            # End-to-end testing
├── packages/
│   ├── ui/             # Shared UI components
│   └── eslint-config/  # Shared ESLint configuration
└── visor-urbano-docs/  # This documentation
```

## 🌍 Multi-City Support

Visor Urbano is designed to support multiple cities and countries:

- **Configurable legal frameworks** per jurisdiction
- **Adaptable GIS layers** for different urban data
- **Flexible permit types** and workflow processes
- **Multi-language support** (Spanish, English, French, Portuguese)

## 🤝 Contributing

### Code Standards

- Follow established patterns in similar components/routes
- Use TypeScript strictly - no `any` types
- Write comprehensive tests for new features
- Document APIs thoroughly in Swagger
- Follow semantic commit conventions

### Development Workflow

1. **Branch from main** for new features
2. **Test locally** with all development servers running
3. **Run test suites** before committing
4. **Update documentation** for API/component changes
5. **Create pull request** with clear description

## 📋 Best Practices

### Frontend Development

- Use existing UI components from the design system
- Follow established routing patterns
- Implement proper error handling and loading states
- Ensure responsive design on all screen sizes
- Write Storybook stories for reusable components

### Backend Development

- Document all endpoints with clear examples
- Use proper HTTP status codes
- Implement comprehensive error handling
- Write unit tests for business logic
- Follow REST API conventions

### Database

- Use migrations for schema changes
- Index spatial queries appropriately
- Consider performance implications of GIS operations
- Backup strategies for production deployments

## 🔧 Common Development Tasks

### Starting Development Environment

```bash
# Start all services
pnpm dev

# Start individual services
pnpm dev:frontend    # React app
pnpm dev:backend     # FastAPI server
pnpm dev:docs        # Docusaurus
pnpm storybook       # Storybook
```

### Testing

```bash
# Run all tests
pnpm test

# Run specific test suites
pnpm test:frontend   # Frontend unit tests
pnpm test:backend    # Backend tests
pnpm test:e2e        # End-to-end tests
```

### Building for Production

```bash
# Build all applications
pnpm build

# Build specific applications
pnpm build:frontend
pnpm build:backend
pnpm build:docs
```

## 🐛 Troubleshooting

### Common Issues

1. **PostGIS Extension Not Found**

   - Ensure PostgreSQL with PostGIS is properly installed
   - Check database connection strings

2. **Frontend Build Errors**

   - Clear node_modules and reinstall dependencies
   - Check TypeScript configuration

3. **Backend Import Errors**

   - Verify Python virtual environment is activated
   - Check all required packages are installed

4. **Storybook Not Loading**
   - Ensure frontend build is successful first
   - Check for conflicting port usage

### Getting Help

- Check existing documentation in this section
- Review similar implementations in the codebase
- Ask questions in team communication channels
- Create detailed issues for bugs or feature requests

## 📈 Performance Considerations

### Frontend Performance

- Use React Query for efficient data fetching
- Implement proper component memoization
- Optimize bundle size with code splitting
- Use proper image optimization techniques

### Backend Performance

- Implement database query optimization
- Use proper indexing for spatial queries
- Consider caching strategies for static data
- Monitor API response times

### GIS Performance

- Use appropriate spatial indexes
- Optimize geometry simplification for different zoom levels
- Consider tile-based serving for large datasets
- Implement proper coordinate system transformations

---

Happy coding! 🚀

For specific implementation details, explore the other documents in this development section.
