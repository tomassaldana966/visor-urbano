# Visor Urbano - Agreed-Upon Features Specification

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Core Platform Features](#core-platform-features)
3. [User Management & Authentication](#user-management--authentication)
4. [Interactive Mapping System](#interactive-mapping-system)
5. [Business License Management](#business-license-management)
6. [Urban Planning & Procedures](#urban-planning--procedures)
7. [Document Management](#document-management)
8. [Analytics & Reporting](#analytics--reporting)
9. [Administrative Functions](#administrative-functions)
10. [Technical Infrastructure](#technical-infrastructure)
11. [Integration Capabilities](#integration-capabilities)
12. [Security & Compliance](#security--compliance)

## Executive Summary

Visor Urbano is a comprehensive municipal urban planning and management platform built with modern technologies (React 19, FastAPI, PostgreSQL/PostGIS). This document details the complete feature set currently implemented and validated across municipal deployments, providing a definitive reference for cities evaluating or implementing the platform.

### Platform Metrics

- **Backend Coverage**: 78% (214+ comprehensive tests)
- **Frontend Components**: 35+ components with TypeScript
- **API Endpoints**: 80+ REST endpoints across 15+ routers
- **Test Coverage**: 150+ frontend tests, 214+ backend tests
- **Technology Stack**: React 19, Vite 6, FastAPI, Python 3.13, PostgreSQL/PostGIS
- **Deployment Status**: Production-ready with Docker support

### Current Implementation Status

**✅ Fully Implemented:**

- Business License Management (complete workflow)
- Interactive Mapping System (OpenLayers with GIS)
- User Authentication & Role Management
- Document Upload & Management
- Municipal Administration Dashboard

**🚧 In Development:**

- Building Permits (basic functionality available)
- Advanced Construction Workflow
- Enhanced Reporting Features

**📅 Planned:**

- Additional Municipal Procedures
- Advanced Analytics Dashboard
- Mobile Application

## Core Platform Features

### 1. Municipal Management Dashboard

- **Real-time metrics** for procedure tracking
- **Activity feed** with configurable notifications
- **Quick actions panel** for common administrative tasks
- **Workflow visualization** with department assignments
- **Performance analytics** with customizable date ranges

### 2. Multi-User Role System

- **Citizens**: Public application submission and tracking
- **Municipal Staff**: Procedure review and processing
- **Directors**: Administrative oversight and configuration
- **Reviewers/Technicians**: Field validation and reporting
- **System Administrators**: Full platform management

### 3. Responsive Web Interface

- **Mobile-first design** with Tailwind CSS
- **Responsive layout** compatible with desktop and mobile devices
- **Multi-language support** (Spanish, English, French, Portuguese)
- **Accessibility compliance** (WCAG 2.1)
- **Dark/light mode** theme switching

## User Management & Authentication

### Authentication System

- **JWT-based authentication** with secure token handling
- **Role-based access control** (RBAC) with granular permissions
- **Password recovery** via email with secure token validation
- **Session management** with automatic timeout
- **Secure password storage** with bcrypt hashing

### User Roles & Permissions

```yaml
Citizen:
  - Submit new procedures
  - Track application status
  - Download certificates
  - Upload required documents
  - Receive notifications

Municipal Staff:
  - Review applications
  - Request additional documentation
  - Schedule inspections
  - Update procedure status
  - Generate reports

Director:
  - Approve/reject applications
  - Configure workflows
  - Manage users and roles
  - Access analytics dashboard
  - System configuration

Reviewer/Technician:
  - Conduct field inspections
  - Upload inspection reports
  - Update compliance status
  - Review technical specifications
```

### Account Management

- **User profile management** with contact information
- **Document upload history** with versioning
- **Notification preferences** configuration
- **Activity audit logs** for security tracking
- **Password change** functionality

## Interactive Mapping System

### GIS Capabilities

- **OpenLayers integration** for high-performance mapping
- **Multi-layer support** with WMS/WFS protocols
- **Spatial analysis tools** for zoning compliance
- **Drawing and measurement tools** for property definition
- **Geocoding services** for address validation

### Map Layers Management

```typescript
Map Layers Available:
- Base Maps: Satellite imagery, street maps, topographic
- Zoning Layers: Primary and secondary zoning (2023)
- Infrastructure: Road networks, utilities, public facilities
- Property Boundaries: Cadastral information with ownership data
- Environmental: Protected areas, flood zones, soil types
- Development: Approved projects, construction sites
```

### Geospatial Features

- **Property information popup** with detailed data
- **Zoning verification** with automatic compliance checking
- **Buffer analysis** for setback requirements
- **Spatial search** by address, coordinates, or property ID
- **Map printing** with customizable layouts

### Layer Configuration

- **Municipality-specific layers** with custom styling
- **Layer visibility controls** with opacity adjustment
- **WMS server integration** with external data sources
- **Custom symbol libraries** for municipal standards
- **Real-time data updates** via WebSocket connections

## Business License Management

### License Generation System

- **Dual generation methods**: System-generated and scanned upload
- **Unified backend storage** for all license types
- **Multi-signature support** with dynamic selection
- **QR code generation** for verification
- **Template-based rendering** with HTML/CSS to PDF

### License Types Supported

```yaml
Business Licenses: ✅ Commercial operation permits (Full implementation)
  ✅ Business activities by SCIAN code (622+ activities)
  ✅ Alcohol sales permits (Integrated)
  ✅ Food service permits (Available)
  🚧 Construction permits (Basic implementation)
  📅 Environmental compliance certificates (Planned)
  📅 Public event permits (Planned)
  📅 Professional service licenses (Planned)
```

**Note**: Currently the system is fully optimized for business/commercial licenses. Building permits are in development with basic functionality available.

### License Workflow

1. **Application Submission** with required documentation
2. **Document Validation** by municipal staff
3. **Technical Review** by specialized departments
4. **Inspection Scheduling** if required
5. **Approval Decision** with justification
6. **License Generation** with official signatures
7. **Digital Delivery** with verification QR code

### Electronic Signatures

- **Digital certificate support** (.cer/.key files)
- **OpenSSL integration** for secure processing
- **CURP validation** for Mexican tax ID verification
- **Audit trail maintenance** with metadata storage
- **Signature verification** with public key validation

## Urban Planning & Procedures

### Procedure Management

- **Workflow engine** with configurable steps
- **Department routing** with automatic assignments
- **Deadline tracking** with escalation alerts
- **Document requirements** by procedure type
- **Conditional logic** for complex approval paths

### Supported Procedures

```yaml
✅ Business Licenses (Fully Implemented):
  - Commercial operation permits
  - Business activity licenses (SCIAN-based)
  - Alcohol sales authorization
  - Food service permits
  - Professional business permits

🚧 Construction Permits (In Development):
  - Basic permit application
  - Document upload
  - Review workflow
  - Simple approval process

📅 Future Procedures (Planned):
  - Residential construction
  - Commercial development
  - Infrastructure projects
  - Land use changes
  - Environmental assessments
```

### Workflow Configuration

- **Multi-step approval processes** with dependencies
- **Parallel review capabilities** for efficiency
- **Department-specific assignments** with expertise matching
- **Legal foundation tracking** for compliance
- **Processing time estimates** with SLA monitoring

### Dependency Management

- **Prerequisite procedures** with status validation
- **Cross-procedure integration** for comprehensive approval
- **External agency coordination** with status synchronization
- **Document sharing** between related procedures

## Document Management

### File Upload System

- **Secure file storage** with virus scanning
- **Version control** for document revisions
- **Multiple format support** (PDF, images, CAD files)
- **File size limits** with compression options
- **Metadata extraction** for searchable indexing

### Document Types

```yaml
Required Documents:
  - Official identification
  - Property deeds
  - Technical drawings
  - Environmental studies
  - Insurance certificates
  - Payment receipts
  - Previous permits

Generated Documents:
  - Approval certificates
  - Inspection reports
  - Technical sheets
  - Payment orders
  - Notification letters
```

### Document Security

- **Encrypted storage** with access logging
- **Digital watermarks** for authenticity
- **Access permissions** by user role
- **Retention policies** with automatic archival
- **Backup systems** with disaster recovery

## Analytics & Reporting

### Dashboard Metrics

- **Real-time KPIs** with trend analysis
- **Procedure volumes** by type and status
- **Processing times** with bottleneck identification
- **User activity** with engagement metrics
- **Geographic distribution** of applications

### Report Generation

```typescript
Available Reports:
- Procedure Status Summary
- Department Performance Analysis
- Geographic Application Distribution
- Revenue Collection Summary
- Processing Time Analysis
- User Activity Report
- Compliance Audit Report
```

### Data Visualization

- **Interactive charts** with drill-down capabilities
- **Geographic heat maps** for spatial analysis
- **Time series analysis** for trend identification
- **Comparative analysis** across periods
- **Export capabilities** (PDF, Excel, CSV)

### Performance Monitoring

- **SLA tracking** with breach alerts
- **Department efficiency** metrics
- **Resource utilization** analysis
- **Citizen satisfaction** scoring
- **Revenue impact** assessment

## Administrative Functions

### System Configuration

- **Municipality settings** with custom branding
- **Workflow configuration** with visual editor
- **User role management** with permission matrices
- **Department structure** with hierarchy definition
- **Business rules** with validation logic

### Content Management

- **News and announcements** with rich text editor
- **Public information** pages with version control
- **FAQ management** with search capabilities
- **Help documentation** with multimedia support
- **Contact information** with department routing

### Notification System

- **Email notifications** with template customization
- **In-app notifications** with read status tracking
- **Subscription management** by notification type
- **Email delivery confirmation** with retry mechanisms

## Technical Infrastructure

### Architecture Stack

```yaml
Frontend:
  - React 19 with TypeScript 5.7+
  - Vite 6.2+ build system
  - React Router v7.6
  - Tailwind CSS 4.0+
  - OpenLayers for mapping
  - Storybook for components

Backend:
  - FastAPI with Python 3.13
  - PostgreSQL with PostGIS
  - SQLAlchemy 2.0+ with Alembic
  - authlib for JWT authentication (replaces python-jose)
  - WeasyPrint for PDF generation
  - SendGrid email integration

Development:
  - Turborepo monorepo
  - pnpm 9.0+ package management
  - Vitest 3.0+ testing
  - Playwright E2E tests
  - GitHub Actions CI/CD
```

### Database Schema

- **Normalized relational design** with spatial support
- **Migration system** with version control
- **Backup strategies** with point-in-time recovery
- **Performance indexing** for spatial queries
- **Data integrity** with foreign key constraints

### Deployment Options

- **Docker containerization** with compose files (available for both frontend and backend)
- **Local development** with environment configuration
- **Standard cloud deployment** (requires additional configuration)
- **On-premise installation** with PostgreSQL/PostGIS database

## Integration Capabilities

### API Architecture

- **RESTful API design** with OpenAPI documentation
- **Swagger UI** for interactive testing
- **JWT authentication** with role-based access control
- **Request/response validation** with Pydantic models
- **Auto-generated API documentation** with endpoint descriptions

### External System Integration

```yaml
Email Services:
  - SendGrid (implemented)
  - SMTP configuration

File Storage:
  - Local file system storage
  - Document upload handling

Mapping Services:
  - OpenLayers integration
  - WMS/WFS protocols
  - Custom GeoServer layers

Database Systems:
  - PostgreSQL with PostGIS
  - Spatial data support
```

### Data Exchange

- **Standard formats** (GeoJSON, KML, Shapefile)
- **API versioning** with backward compatibility
- **Bulk data operations** with batch processing
- **Real-time synchronization** with change notifications
- **Data validation** with schema enforcement

## Security & Compliance

### Security Features

- **HTTPS enforcement** with SSL/TLS certificates
- **SQL injection protection** with parameterized queries
- **XSS prevention** with content sanitization
- **CSRF protection** with token validation
- **Input validation** with schema checking

### Data Privacy

- **Data protection** with secure storage practices
- **Access logging** for audit trails
- **Secure data transmission** with HTTPS enforcement
- **Password security** with bcrypt hashing

### Vulnerability Management

- **Regular security scanning** with automated monitoring
- **Dependency updates** with vulnerability tracking
- **Penetration testing** with external validation
- **Security incident response** with documented procedures
- **Compliance reporting** with audit trails

### Access Control

- **Role-based permissions** with least privilege principle
- **Session management** with automatic timeouts
- **Activity monitoring** with security logging
- **Secure authentication** with JWT tokens

## Feature Validation Status

### Testing Coverage

```yaml
Backend Testing:
  - Line Coverage: 78%
  - Test Files: 214+ comprehensive tests
  - Business Logic: Complete coverage
  - API Endpoints: All endpoints tested
  - Security: Authentication and authorization tested

Frontend Testing:
  - Component Tests: 11 test files (150+ tests)
  - Storybook Stories: 35+ components (100% coverage)
  - E2E Tests: Core user journeys
  - Visual Regression: Automated screenshot testing
  - Performance: Lighthouse score optimization

Quality Assurance:
  - Code Quality: ESLint, Prettier, TypeScript
  - Security Scanning: Snyk integration
  - Dependency Management: Automated updates
  - Documentation: 100% API documentation
  - Deployment: Automated CI/CD pipelines
```

### Production Readiness

- **Containerized deployment** with Docker support
- **Database migrations** with Alembic
- **Environment configuration** with environment variables
- **Error handling** with comprehensive logging
- **API documentation** with OpenAPI/Swagger

## Municipal Adaptation

### Configuration Options

- **Branding customization** with logos and colors
- **Language localization** with translation management
- **Legal framework** adaptation by jurisdiction
- **Workflow customization** for local procedures
- **Integration mapping** for existing systems

---

This specification represents the complete feature set of Visor Urbano as validated through comprehensive testing and municipal deployments. Features are categorized by implementation status to provide accurate expectations for municipal adoption.
