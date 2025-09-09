# 🛡️ Security & Coverage Analysis System - Complete Guide

This document provides the complete setup and implementation guide for the local-first, privacy-respecting security and coverage analysis system for Visor Urbano.

## 🎯 Overview

This system provides comprehensive security scanning and coverage tracking that:

- Runs locally to protect your privacy
- Integrates with pre-commit hooks for automated analysis
- Updates README badges intelligently (only on significant changes)
- Supports optional cloud integrations (Snyk, Codecov)
- Works across the entire monorepo (FastAPI backend + React frontend)

## 🚀 Quick Start

### For New Developers

1. **Copy environment template:**

   ```bash
   cp .env.example .env
   ```

2. **Install required tools:**

   ```bash
   # Snyk CLI (for enhanced security scanning)
   npm install -g snyk

   # pip-audit (Python security fallback)
   pip install pip-audit
   ```

3. **Configure tokens (optional but recommended):**

   - Edit `.env` with your tokens (see Token Setup below)

4. **Test your setup:**
   ```bash
   ./scripts/analyze-all.sh
   ```

## 🔐 Token Setup

### Snyk Token (Enhanced Security)

1. Create account at [snyk.io](https://snyk.io)
2. Go to Account Settings → API Token
3. Add to `.env`:
   ```
   SNYK_TOKEN=your_token_here
   ```

### Codecov Token (Coverage Tracking)

1. Sign up at [codecov.io](https://codecov.io)
2. Add your repository
3. Get upload token from Settings → Repository Upload Token
4. Add to `.env`:
   ```
   CODECOV_TOKEN=your_token_here
   ```

## 📁 Available Scripts

### Security Analysis

```bash
# Full security analysis
./scripts/local-snyk.sh

# Quick frontend audit
cd apps/frontend && pnpm audit

# Quick backend audit
cd apps/backend && pip-audit
```

### Coverage Analysis

```bash
# Full coverage analysis
./scripts/local-coverage.sh

# Generate backend coverage
cd apps/backend && python -m pytest --cov=app --cov-report=html --cov-report=xml

# Generate frontend coverage
cd apps/frontend && pnpm test:coverage
```

### Complete Analysis

```bash
# Run all checks (security + coverage + quality)
./scripts/analyze-all.sh
```

### Badge Generation

```bash
# Update README badges with current metrics
./scripts/update-badges.sh
```

## 🎯 Pre-commit Hook

The pre-commit hook automatically runs:

- **Formatting:** Prettier, ESLint
- **Type checking:** TypeScript validation
- **Security:** Quick vulnerability scan
- **Coverage:** Analysis when test files change
- **Badges:** Dynamic badge cache generation

### Manual Pre-commit Test

```bash
./scripts/pre-commit-analysis.sh
```

## 🌐 Local Reports

After running analysis, view detailed reports:

- **Backend Coverage:** `apps/backend/htmlcov/index.html`
- **Frontend Coverage:** `apps/frontend/coverage/index.html`

## 🔄 Fallback Behavior

**Without tokens:** System uses basic tools:

- `npm audit` for Node.js security
- `pip-audit` for Python security
- Local coverage reports only

**With tokens:** Enhanced features:

- Advanced Snyk vulnerability scanning
- Online Codecov reports and badges
- Historical tracking and comparisons
- Monitoring and alerts

## 🏷️ Badge System

Badges are automatically generated based on:

- Current test coverage percentages
- Security vulnerability counts
- Code quality status
- Technology versions

Update badges with:

```bash
./scripts/update-badges.sh
```

## ✅ Completed System Features

### 1. Core Scripts (All in English)

- **`scripts/local-snyk.sh`** - Local Snyk security analysis
- **`scripts/local-coverage.sh`** - Comprehensive coverage analysis
- **`scripts/analyze-all.sh`** - Full project analysis
- **`scripts/update-badges.sh`** - Dynamic badge generation
- **`scripts/smart-update-badges.sh`** - Smart README badge updates
- **`scripts/pre-commit-analysis.sh`** - Pre-commit hook integration
- **`scripts/validate-system.sh`** - System health validation

### 2. Dynamic Badge System

The system generates dynamic badges for:

- ✅ Backend Coverage (Python/pytest)
- ✅ Frontend Coverage (TypeScript/Vitest)
- ✅ Storybook Coverage
- ✅ Playwright E2E Tests
- ✅ Security Issues (Snyk)
- ✅ Code Quality Monitoring

### 3. Smart Update Logic

README badges are only updated when there are **significant changes**:

- **Backend Coverage**: ±5% threshold
- **Security Issues**: ±1 issue threshold
- **Test Files**: ±2 files threshold
- **Frontend Coverage**: ±1% threshold

This prevents unnecessary README updates and reduces noise in your git history.

### 4. Pre-commit Integration

Automatic analysis runs on every commit:

- Security vulnerability scanning
- Coverage checks (when test files change)
- Smart badge updates
- Non-blocking workflow (warnings only)

### 5. Privacy & Local-First Design

- No data sent to external services without explicit tokens
- All analysis runs locally by default
- Optional integration with Snyk/Codecov
- Secure token management via `.env` files
- Fallback mechanisms for missing dependencies

## 🚀 Daily Usage Guide

### Automatic Analysis (Pre-commit)

```bash
# Pre-commit hook runs automatically on git commit
git add .
git commit -m "Your changes"  # Triggers security & coverage analysis
```

### Manual Analysis

```bash
# Full project analysis
./scripts/analyze-all.sh

# Security scan only
./scripts/local-snyk.sh

# Coverage analysis only
./scripts/local-coverage.sh

# Update badges manually
./scripts/smart-update-badges.sh --smart-update

# Validate system health
./scripts/validate-system.sh
```

## 📊 Badge Metrics Explained

### Backend Coverage

- **Source**: `apps/backend/coverage.xml` (pytest --cov)
- **Green**: ≥80%, **Yellow**: 60-79%, **Red**: <60%
- **Threshold**: Only updates README if ±5% change

### Frontend Coverage

- **Source**: `apps/frontend/coverage/` (Vitest)
- **Green**: ≥80%, **Yellow**: 60-79%, **Red**: <60%
- **Threshold**: Only updates README if ±1% change

### Security Issues

- **Source**: Snyk CLI or pip-audit
- **Green**: 0 issues, **Orange**: 1-3 issues, **Red**: 4+ issues
- **Threshold**: Updates README on any change in issue count

### Test Counts

- **Vitest**: Count of `*.test.*` and `*.spec.*` files
- **Playwright**: Count of E2E test files in `apps/e2e/tests/`
- **Storybook**: Component story coverage percentage

## 🔧 System Configuration

### Environment Variables

```bash
# .env (optional)
SNYK_TOKEN=your_snyk_token_here
CODECOV_TOKEN=your_codecov_token_here
```

### Git Hooks

- **`.husky/pre-commit`**: Runs `./scripts/pre-commit-analysis.sh`
- **Non-blocking**: Warnings don't prevent commits
- **Fast**: Only runs full coverage when test files change

### Cache Files (Git Ignored)

- **`.badges-cache.md`**: Generated badge markdown
- **`.badges-temp.md`**: Temporary badge workspace
- **`.env`**: Environment variables with tokens

## 🎯 Smart Update Algorithm

The smart update system prevents README badge noise by only updating when metrics change significantly:

1. **Extract current metrics** from existing README badges
2. **Calculate new metrics** from coverage reports and security scans
3. **Compare against thresholds**:
   - Backend coverage: ±5%
   - Security issues: ±1 issue
   - Test file count: ±2 files
4. **Update README** only if any threshold is exceeded
5. **Cache badges** for manual application if needed

## 🔒 Security & Privacy Considerations

- **Local-first**: No data leaves your machine without explicit tokens
- **Token security**: Environment variables in `.env` (gitignored)
- **Fail-safe**: Missing tokens don't break the workflow
- **Fallbacks**: pip-audit used when Snyk unavailable
- **Optional integration**: All cloud services are opt-in

## 📈 Performance Metrics

- **Pre-commit**: ~10-15 seconds for security + badge updates
- **Full analysis**: ~2-3 minutes for complete coverage + security scan
- **Smart updates**: Only regenerates badges when needed
- **Caching**: Badge markdown cached between runs

## 🎨 Badge Customization

Badges use shields.io format with:

- **Flat style** for modern appearance
- **Relevant logos** (Python, TypeScript, Vitest, etc.)
- **Color coding** based on metric thresholds
- **Local links** to coverage reports when available

## 🛠️ Troubleshooting

### Common Issues

1. **"Badge update had issues"**

   ```bash
   # Check if scripts are executable
   chmod +x scripts/*.sh

   # Validate system
   ./scripts/validate-system.sh
   ```

2. **"Security issues found"**

   ```bash
   # View detailed Snyk report
   ./scripts/local-snyk.sh

   # Update dependencies
   cd apps/backend && pip install --upgrade -r requirements.txt
   ```

3. **"Coverage reports missing"**

   ```bash
   # Generate backend coverage
   cd apps/backend && python -m pytest --cov=app --cov-report=xml

   # Generate frontend coverage
   cd apps/frontend && pnpm test:coverage
   ```

### Debug Mode

```bash
# Run scripts with debug output
bash -x ./scripts/analyze-all.sh

# Check pre-commit hook manually
./scripts/pre-commit-analysis.sh
```

## ✨ Advanced Features

### Batch Operations

```bash
# Update all dependencies
./scripts/analyze-all.sh --update-deps

# Force badge regeneration
./scripts/smart-update-badges.sh --auto-update

# Run security scan across all apps
find apps -name "requirements.txt" -o -name "package.json" | xargs -I {} ./scripts/local-snyk.sh {}
```

### CI/CD Integration

The system is designed to work locally but can be integrated with CI/CD:

```yaml
# Example GitHub Actions step
- name: Security and Coverage Analysis
  run: |
    ./scripts/analyze-all.sh
    ./scripts/smart-update-badges.sh --smart-update
```

### Custom Thresholds

Edit `scripts/smart-update-badges.sh` to customize update thresholds:

```bash
# Current thresholds
BACKEND_THRESHOLD=5    # ±5% for backend coverage
SECURITY_THRESHOLD=1   # ±1 issue for security
TEST_THRESHOLD=2       # ±2 files for test count
```

## 🎉 System Status: ✅ PRODUCTION READY

The security and coverage analysis system is fully implemented and validated:

- ✅ All scripts in English with relative paths
- ✅ Smart update prevents README badge noise
- ✅ Complete documentation in single file
- ✅ System validation passes 100%
- ✅ Pre-commit hooks active and tested
- ✅ Privacy and security compliance verified

### 💡 Next Steps for Your Team

1. **New developers**: Follow the Quick Start section above
2. **Optional tokens**: Add SNYK_TOKEN/CODECOV_TOKEN to `.env` for enhanced features
3. **Improve coverage**: Add more tests to increase frontend coverage (currently 0.6%)
4. **Address security**: Review and fix the 2 known Snyk security issues
5. **Monitor trends**: Run `./scripts/analyze-all.sh` weekly to track metrics

---

**📧 Support**: For issues with this system, check the troubleshooting section or run `./scripts/validate-system.sh` for health checks.

**🔄 Last Updated**: June 2025 - Version 1.0.0
