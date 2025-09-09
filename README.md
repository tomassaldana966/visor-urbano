# Visor Urbano

[![GitHub CI](https://github.com/Delivery-Associates/visor-urbano/actions/workflows/test.yml/badge.svg)](https://github.com/Delivery-Associates/visor-urbano/actions/workflows/test.yml)
[![PR Validation](https://github.com/Delivery-Associates/visor-urbano/actions/workflows/validatepr.yml/badge.svg)](https://github.com/Delivery-Associates/visor-urbano/actions/workflows/validatepr.yml)
[![Security Status](https://img.shields.io/badge/security-analyzed-brightgreen?style=flat&logo=shield)](docs/SECURITY_COVERAGE_SETUP.md)
[![Backend Coverage](https://img.shields.io/badge/backend%20coverage-78%25-green?style=flat&logo=python)](apps/backend/htmlcov/index.html)
[![Frontend Coverage](https://img.shields.io/badge/frontend%20coverage-6.1%25-red?style=flat&logo=typescript)](apps/frontend/coverage/index.html)
[![Storybook Coverage](https://img.shields.io/badge/storybook%20coverage-100%25-brightgreen?style=flat&logo=storybook)](http://localhost:6006)
[![Vitest Tests](https://img.shields.io/badge/vitest%20tests-11%20files-yellow?style=flat&logo=vitest)](apps/frontend/coverage/index.html)
[![Code Quality](https://img.shields.io/badge/code%20quality-monitored-blue?style=flat&logo=codacy)](scripts/analyze-all.sh)
[![Snyk Vulnerabilities](https://img.shields.io/badge/snyk-no%20high%20issues-brightgreen?style=flat&logo=snyk)](scripts/local-snyk.sh)
[![TypeScript](https://img.shields.io/badge/typescript-^5.7.2-blue?style=flat&logo=typescript)](apps/frontend/tsconfig.json)
[![Python](https://img.shields.io/badge/python-3.13-blue?style=flat&logo=python)](apps/backend/requirements.txt)

A modern urban planning visualization platform built with FastAPI and React 19, featuring interactive mapping capabilities and comprehensive urban data management.

### Quick Start

📖 **For detailed step-by-step instructions:** See [Developer Setup Guide](docs/visor_urbano_step_by_step.md)

If you’re short on time, follow these quick steps to get up and running:

```bash
# 1. Clone and setup
git clone <repository-url>
cd visor-urbano

# 2. Run the automated setup script
./setup.sh

# 3. Start development
pnpm dev


# 4. Load test data (after setup.sh and 'pnpm dev' completes successfully)
./setup-test-data.sh
```

## 🏗️ Project Structure

This is a monorepo organized using Turborepo with the following applications:

```
visor-urbano/
├── apps/
│   ├── backend/          # FastAPI Python backend
│   ├── frontend/         # React 19 TypeScript frontend
│   └── e2e/             # End-to-end tests with Playwright
├── packages/            # Shared packages and utilities
└── .github/workflows/   # CI/CD with GitHub Actions
```

## 🚀 Technology Stack

### Backend (`apps/backend`)

- **Framework:** FastAPI (Python 3.13)
- **Database:** PostgreSQL with SQLAlchemy and Alembic
- **Geographic Data:** GeoAlchemy2 for spatial data handling
- **Authentication:** JWT with authlib (secure implementation)
- **Validation:** Pydantic v2 with full data validation
- **PDF Generation:** WeasyPrint for license and report generation
- **Template Engine:** Jinja2 for dynamic HTML template rendering
- **Electronic Signatures:** OpenSSL integration for digital certificate processing
- **Email:** SendGrid integration
- **Container:** Docker and Docker Compose

### Frontend (`apps/frontend`)

- **Framework:** React 19 with TypeScript
- **Build System:** Vite for fast development and builds
- **Routing:** React Router v7.6 with data loaders
- **Styling:** Tailwind CSS with custom design system
- **Mapping:** OpenLayers for interactive maps
- **Component Library:** Radix UI primitives
- **Internationalization:** react-i18next
- **Development:** Storybook for component development
- **Testing:** Vitest and Playwright

### Development Tools

- **Monorepo:** Turborepo for task orchestration
- **Package Manager:** pnpm for efficient dependency management
- **Code Quality:** ESLint, Prettier, TypeScript
- **CI/CD:** GitHub Actions with automated testing
- **Testing:** Comprehensive test suite with 214+ Python tests

## 🧪 Testing & Quality Metrics

The project maintains comprehensive testing coverage across multiple tools:

### 📚 Storybook (Component Documentation)

- **Coverage:** 100% (35/35 components)
- **Purpose:** Interactive component development and documentation
- **Access:** `pnpm dev` → http://localhost:6006
- **Status:** ✅ Excellent - All components have stories

### 🧪 Vitest (Unit Testing)

- **Current:** 11 test files (150 tests)
- **Purpose:** Fast unit tests for TypeScript/JavaScript code
- **Command:** `pnpm test:vitest`
- **Recent Additions:** IssueLicenseModal, Business Types API, Director utilities, Zod validation
- **Status:** ✅ Good progress - Significant improvement from 3 to 11 test files

### 🎭 Playwright (E2E Testing)

- **Current:** 1 E2E test
- **Purpose:** End-to-end browser automation testing
- **Command:** `pnpm test` (in apps/e2e)
- **Status:** ⚠️ Needs improvement - Add more E2E scenarios

### 📊 Coverage Metrics

- **Backend:** 78% line coverage (7,418 statements, 1,629 missed)
- **Frontend:** 6.1% line coverage (150 tests across 11 test files)
- **Business Logic:** Comprehensive coverage of license generation, electronic signatures, and procedure workflows
- **Recent Frontend Improvements:** 10x improvement in coverage (0.6% → 6.1%) with new component and utility tests
- **Overall:** Strong backend coverage with comprehensive business logic testing, frontend showing significant improvement

## 🔒 Security Status

The project maintains a strong security posture with regular vulnerability monitoring:

### ✅ Recent Security Improvements (June 2025)

- **JWT Security:** Migrated from `python-jose` to `authlib` (eliminated 2 CVEs)
- **Dependency Updates:** Updated to latest secure versions
- **Vulnerability Monitoring:** Automated security scanning with documented mitigations

### ⚠️ Known Security Issues (Monitored)

- **ECDSA Library:** 2 vulnerabilities in `ecdsa@0.19.1` (required by SendGrid)
  - CVE-2024-23342 (Minerva attack)
  - PVE-2024-64396 (Side-channel attack)
  - **Risk Level:** Low (contained to email operations only)
  - **Status:** Documented and monitored for updates

### 🛡️ Security Measures

- **Authentication:** Secure JWT implementation with `authlib`
- **Monitoring:** Weekly security scans and dependency updates
- **Documentation:** Complete security documentation in [`SECURITY_VULNERABILITIES.md`](apps/backend/SECURITY_VULNERABILITIES.md)
- **Scripts:** Automated security monitoring via [`security_monitor.py`](apps/backend/scripts/security_monitor.py)

For detailed security information, see our [Security Documentation](apps/backend/SECURITY_VULNERABILITIES.md)

## 📋 Prerequisites

- **Node.js:** 18+ (specified in package.json engines)
- **Python:** 3.13
- **pnpm:** 9.0.0+ (specified as packageManager)
- **Docker:** For containerized backend development

## 🛠️ Installation & Setup

### 1. Clone and Install Dependencies

```bash
git clone [repository-url]
cd visor-urbano
pnpm install
```

### 2. Backend Setup

```bash
cd apps/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start with Docker (recommended)
npm run dev  # Builds and starts PostgreSQL + FastAPI

# Or start manually
npm run start  # Uses existing containers
```

### 3. Frontend Setup

```bash
cd apps/frontend

# Development mode (includes Storybook)
pnpm dev

# Production build
pnpm build

# Start production server
pnpm start
```

## 🏃‍♂️ Development Commands

### Monorepo Commands (from root)

```bash
pnpm dev        # Start all applications
pnpm build      # Build all applications
pnpm test       # Run all tests
pnpm lint       # Lint all applications
pnpm format     # Format code with Prettier
```

### Backend Commands

```bash
cd apps/backend
npm run dev     # Docker Compose build + start
npm run start   # Start existing containers
pytest          # Run 214+ Python tests
```

### Frontend Commands

```bash
cd apps/frontend
pnpm dev                 # Dev server + Storybook
pnpm storybook          # Storybook only
pnpm test               # Vitest + Storybook tests
pnpm build              # Production build
pnpm typecheck          # TypeScript checking
```

## 🧪 Testing

### Backend Testing

- **Framework:** pytest with asyncio support
- **Coverage:** 78% line coverage with 214+ comprehensive tests
- **Database:** Test database isolation with fixtures
- **License Generation:** Complete testing of both scanned and system-generated licenses
- **Electronic Signatures:** Comprehensive validation and security testing
- **Status:** ✅ All tests passing with zero warnings

### Frontend Testing

- **Unit Tests:** Vitest for component and utility testing
- **Component Tests:** Storybook test runner for component stories
- **E2E Tests:** Playwright for end-to-end testing
- **Visual Testing:** Storybook for visual regression testing

### CI/CD Pipeline

- **GitHub Actions:** Automated testing on push/PR
- **Python Tests:** Runs pytest with full backend validation
- **Node.js Tests:** Frontend and E2E test execution
- **Multi-environment:** Validates across different environments

## 🌍 Features

### Interactive Mapping

- **OpenLayers Integration:** High-performance web mapping
- **Multiple Layer Support:** WMS, GeoServer, and custom layers
- **Drawing Tools:** Measurement and annotation capabilities
- **Geospatial Analysis:** Built-in spatial data processing

### Urban Planning Tools

- **Zoning Management:** Interactive zoning layer controls
- **Property Information:** Detailed property data visualization
- **Business Licensing:** Unified licensing workflow with dual generation methods
- **Procedure Tracking:** Multi-step approval processes with automated dependency assignment

### Business License Generation (New System)

- **Unified License Handling:** Both system-generated and scanned licenses use identical backend storage and frontend display
- **Dual Generation Methods:**
  - **System Generated:** HTML templates with WeasyPrint PDF generation
  - **Scanned Upload:** Manual PDF upload with form validation
- **Multi-Signature Support:** Dynamic signature selection from municipality signatures
- **Smart Defaults:** Auto-selects "Generate by Visor Urbano" option
- **Complete Form Validation:** Required fields validation for both license types
- **Template Features:**
  - English-language HTML templates with project color scheme
  - QR code generation for license verification
  - Responsive design for PDF generation
  - Local file path handling for images (prevents WeasyPrint timeouts)
- **URL Configuration:** All URLs use configurable `APP_URL` setting (no hardcoded values)

### Electronic Signatures & Security

- **Business Signatures:** Comprehensive electronic signature workflow for procedures
- **CURP Validation:** Mexican tax ID validation for signature authenticity
- **Digital Certificate Support:** .cer and .key file handling with OpenSSL integration
- **Secure File Processing:** Temporary directory creation with proper permissions
- **Audit Trail:** Complete signature metadata tracking with JSON response storage

### User Experience

- **Responsive Design:** Mobile-first approach with Tailwind CSS
- **Multilingual Support:** i18next integration
- **Component Library:** Consistent design system with Storybook
- **Performance Optimized:** Vite build system and code splitting

## 🐳 Docker Support

### Backend Docker Setup

```bash
cd apps/backend
docker compose up    # PostgreSQL + FastAPI
```

### Frontend Docker Setup

```bash
cd apps/frontend
docker compose up    # Production-ready container
```

## 📁 Key Directories

### Backend Structure

```
apps/backend/
├── app/
│   ├── controllers/  # Business logic controllers
│   ├── models/       # SQLAlchemy database models
│   ├── routers/      # FastAPI route definitions
│   ├── schemas/      # Pydantic data models (modernized)
│   ├── services/     # Business logic services
│   ├── utils/        # Utility functions and helpers
│   └── main.py       # FastAPI application entry point
├── config/           # Application configuration
├── migrations/       # Alembic database migrations
├── scripts/          # Database seeding and utility scripts
├── templates/        # HTML templates for PDF generation
│   └── licenses/     # Business license templates (English)
├── tests/            # Comprehensive test suite (214+ tests)
├── uploads/          # File upload directory
│   ├── licenses/     # Generated and uploaded license PDFs
│   └── procedures/   # Procedure-related document uploads
├── requirements.txt  # Python dependencies
└── docker-compose.yaml
```

### Frontend Structure

```
apps/frontend/
├── app/
│   ├── components/   # Reusable UI components
│   ├── containers/   # Container components
│   ├── hooks/        # Custom React hooks
│   ├── lib/          # Utility libraries and configurations
│   ├── routes/       # React Router pages
│   ├── store/        # State management
│   ├── utils/        # Utility functions and API clients
│   ├── assets/       # Static assets and resources
│   └── i18n.ts       # Internationalization setup
├── .storybook/       # Storybook configuration
├── config/           # Application configuration
├── docs/             # Documentation
├── public/           # Static public assets
└── patches/          # Package patches
```

### 🏗️ [Database Architecture Overview](docs/DATABASE_ARCHITECTURE.md)

**Comprehensive architectural documentation:**

- Complete entity documentation with detailed relationships
- Database technology stack (PostgreSQL, PostGIS, SQLAlchemy)
- Multi-tenant architecture patterns
- Security framework and performance optimization
- Migration strategy and backup/recovery procedures

### 🔧 [FastAPI Models & Alembic Guide](docs/FASTAPI_MODELS_ALEMBIC_GUIDE.md)

**Detailed implementation guide:**

- SQLAlchemy model patterns and best practices
- Pydantic schema integration with FastAPI
- Alembic migration management and workflows
- Database session handling and dependency injection
- Testing strategies and performance optimization

### 📈 [Entity Relationship Diagrams](docs/DATABASE_ERD.md)

**Visual database structure documentation:**

- Complete ERD with all 40+ entities and relationships
- Simplified core entity diagrams for quick reference
- Workflow process diagrams showing business logic flow
- Schema evolution timeline and data flow architecture

### 📋 [Database Tables Inventory](docs/DATABASE_TABLES_INVENTORY.md)

**Complete catalog of all database tables:**

- Comprehensive inventory of 82+ database tables organized by functional category
- Detailed purpose and use case explanation for each table
- Key relationships and business logic documentation
- Table statistics, usage patterns, and critical table identification

### 🎯 Key Database Features

- **Multi-tenant Architecture**: Municipality-based data isolation
- **Spatial Data Support**: PostGIS integration for geospatial operations
- **Comprehensive Relationships**: 40+ entities with complex business relationships
- **Audit Trails**: Complete change tracking and soft deletion
- **Performance Optimized**: Spatial indexes and query optimization
- **Migration Ready**: Alembic-based schema version control

### 🚀 For Developers

- **New to the Project?** Start with the [Database Documentation Index](docs/DATABASE_DOCUMENTATION_INDEX.md)
- **Need Visual Understanding?** Check the [Entity Relationship Diagrams](docs/DATABASE_ERD.md)
- **Working on API Development?** Reference the [FastAPI Models & Alembic Guide](docs/FASTAPI_MODELS_ALEMBIC_GUIDE.md)
- **Database Administration?** Focus on the [Database Architecture Overview](docs/DATABASE_ARCHITECTURE.md)
- **Looking for Specific Tables?** Browse the [Database Tables Inventory](docs/DATABASE_TABLES_INVENTORY.md)

## 🔧 Recent Updates

### ✅ Frontend Testing Improvements (January 2025)

- **Test Coverage Expansion:** Added 8 new test files, bringing total from 3 to 11 test files
- **Component Testing:** Added comprehensive tests for IssueLicenseModal, Button, Switch, and LicensesTable components
- **API Testing:** Added thorough testing for business types, reports, and director API utilities
- **Utility Testing:** Added validation tests for date utilities and Zod schema validation
- **Coverage Improvement:** Increased frontend coverage from 0.6% to 6.1% (10x improvement)
- **Test Quality:** 150 total tests with focused coverage on business-critical components

### ✅ Business License System Overhaul (January 2025)

- **Unified License Generation:** Refactored backend to handle both system-generated and scanned licenses identically
- **Dynamic URL Configuration:** Replaced all hardcoded URLs with configurable `APP_URL` setting
- **English Templates:** Created modern, responsive HTML templates with project branding
- **Multi-Signature Support:** Added dynamic signature selection with municipality signature integration
- **Enhanced Frontend Modal:** Auto-selects generation method with comprehensive form validation
- **PDF Generation Improvements:** Local file path handling prevents WeasyPrint timeout issues
- **Comprehensive Error Handling:** Robust validation and error recovery for license generation
- **Template Features:** QR code generation, responsive design, and Red Hat Display font integration

### ✅ Electronic Signatures System (January 2025)

- **Business Signature Workflow:** Complete electronic signature implementation for procedures
- **Security Features:** CURP validation, digital certificate handling, and secure temporary file processing
- **Database Integration:** Comprehensive signature metadata storage with audit trails
- **API Endpoints:** Full CRUD operations for business signatures with role-based access
- **Testing Coverage:** Extensive test suite covering validation, file processing, and error scenarios

### 📡 New API Endpoints (Business License System)

#### License Generation

- `POST /v1/procedures/generate-license/{encoded_folio}` - Generate license automatically by system
- `POST /v1/procedures/issue-license/{encoded_folio}` - Issue license by uploading scanned PDF
- `GET /v1/procedures/licenses-issued` - List all issued licenses with pagination
- `GET /v1/procedures/license/{license_id}/download` - Download license PDF

#### Electronic Signatures

- `POST /v1/electronic_signature/` - Create electronic signature for procedures
- `GET /v1/electronic_signature/` - List business signatures with filtering
- `GET /v1/electronic_signature/{signature_id}` - Get specific signature details

#### Municipality Signatures

- `GET /v1/municipalities/{municipality_id}/signatures` - Get signatures for municipality
- `POST /v1/municipalities/{municipality_id}/signatures` - Create new signature
- `PUT /v1/municipalities/{municipality_id}/signatures/{signature_id}` - Update signature

### ✅ Pydantic V2 Migration (Completed)

- Migrated from Pydantic V1 to V2 patterns
- Updated Field examples: `Field(example="value")` → `Field(json_schema_extra={"example": "value"})`
- Modernized Config: `class Config` → `model_config = ConfigDict()`
- **Result:** Zero deprecation warnings, 214+/214+ tests passing

### ✅ CI/CD Enhancement (Completed)

- Added Python 3.13 testing to GitHub Actions
- Integrated pytest execution with comprehensive validation
- Enhanced workflow with both Node.js and Python testing
- **Result:** Robust CI/CD pipeline for monorepo

### ✅ Code Quality (Completed)

- Fixed all linting and type checking issues
- Standardized code formatting across the monorepo
- Updated development tooling for optimal DX
- **Result:** Clean, maintainable codebase

## 🛠️ Development Setup

### Configuration

#### Backend Configuration (`apps/backend/config/settings.py`)

Key environment variables for the backend:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/visor_urbano

# Application URLs (Important for License Generation)
APP_URL=http://localhost:8000  # Base URL for API and file serving
APP_BASE_URL=http://localhost:8000/  # Base URL with trailing slash

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# Email Configuration (SendGrid)
SENDGRID_API_KEY=your-sendgrid-key

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB in bytes
UPLOAD_DIR=uploads/
```

#### Frontend Configuration (`apps/frontend/.env`)

```bash
# API Configuration
VITE_API_URL=http://localhost:8000  # Backend API URL

# Development
VITE_DEV_PORT=5173
```

**Important:** The `APP_URL` setting is crucial for the new business license system. It's used for:

- QR code generation in licenses
- Image URLs in PDF templates
- File serving URLs
- Email notification links

### Quick Start (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd visor-urbano

# Run the automated setup script
./setup.sh
```

The setup script will:

- Install all dependencies with pnpm
- Configure Git hooks for code quality
- Set up pre-commit hooks for automatic formatting and type checking

### Manual Setup

If you prefer manual setup or the script doesn't work:

```bash
# Install dependencies
pnpm install

# Setup Git hooks manually
pnpm exec husky
ln -sf ../../.husky/pre-commit .git/hooks/pre-commit
```

### Git Hooks Configured

**Pre-commit Hook:**

- ✅ Automatic code formatting with Prettier
- ✅ TypeScript type checking
- ✅ Security vulnerability scanning
- ✅ Test coverage validation (when test files change)
- ✅ Dynamic badge generation
- ✅ Runs only on staged files for performance
- ✅ Prevents commits with formatting, type, or security errors

### 🔐 Security & Coverage Tokens Setup

**For New Developers:** To enable enhanced security scanning and coverage reporting, you'll need to configure optional tokens:

#### 1. Copy Environment Template

```bash
cp .env.example .env
```

#### 2. Get Your Tokens (Optional but Recommended)

**Snyk Token** (for advanced security scanning):

1. Create a free account at [snyk.io](https://snyk.io)
2. Go to Account Settings → API Token
3. Copy your token and add to `.env`:
   ```
   SNYK_TOKEN=your_snyk_token_here
   ```

**Codecov Token** (for coverage upload and tracking):

1. Sign up at [codecov.io](https://codecov.io)
2. Add your repository and get the upload token
3. Add to `.env`:
   ```
   CODECOV_TOKEN=your_codecov_token_here
   ```

#### 3. Verify Setup

```bash
# Test security analysis
./scripts/local-snyk.sh

# Test coverage analysis
./scripts/local-coverage.sh

# Run complete analysis
./scripts/analyze-all.sh
```

**Without tokens:** The system automatically falls back to `pip install safety && safety scan` and `npm audit` for basic security scanning.

**With tokens:** You get enhanced vulnerability scanning, online coverage reports, historical tracking, and monitoring.

**Security Monitoring:** Even without external tokens, the project includes built-in security monitoring:

```bash
# Run our custom security monitor
cd apps/backend && python scripts/security_monitor.py

# Check for vulnerabilities with Safety
cd apps/backend && safety scan
```

This ensures all code in the repository maintains consistent quality, security, and formatting standards.

## 📄 License

TBD
