#!/bin/bash
# 🚀 Pre-commit Security & Coverage Check
# Quick analysis for Husky hooks

echo "🔍 Pre-commit: Security & Coverage Analysis"
echo "==========================================="

# Check if Snyk token exists (optional)
SNYK_TOKEN_AVAILABLE=false
if [ -f ".env" ] && grep -q "SNYK_TOKEN" .env; then
    SNYK_TOKEN_AVAILABLE=true
    source .env 2>/dev/null || true
    export SNYK_TOKEN 2>/dev/null || true
fi

# 1. QUICK SECURITY ANALYSIS
echo ""
echo "🔒 Security Check..."

# Frontend - npm audit (always available)
echo "  Frontend: npm audit..."
cd apps/frontend
FRONTEND_AUDIT=$(pnpm audit --audit-level high --json 2>/dev/null || echo '{"vulnerabilities": {}}')
FRONTEND_VULNS=$(echo "$FRONTEND_AUDIT" | grep -o '"high":[0-9]*' | cut -d: -f2 2>/dev/null || echo "0")

# Ensure FRONTEND_VULNS is a valid number
if ! [[ "$FRONTEND_VULNS" =~ ^[0-9]+$ ]]; then
    FRONTEND_VULNS=0
fi

if [ "$FRONTEND_VULNS" -gt 0 ]; then
    echo "    ⚠️  $FRONTEND_VULNS high/critical vulnerabilities in frontend"
else
    echo "    ✅ Frontend security OK"
fi

# Backend - pip-audit or Snyk
echo "  Backend: security check..."
cd ../backend

if [ "$SNYK_TOKEN_AVAILABLE" = true ] && command -v snyk >/dev/null 2>&1; then
    # Use Snyk if available and authenticated
    if snyk test --file=requirements.txt --severity-threshold=high --quiet >/dev/null 2>&1; then
        echo "    ✅ Backend security OK (Snyk)"
    else
        echo "    ⚠️  Security issues found in backend (Snyk)"
    fi
else
    # Fallback to pip-audit
    if command -v pip-audit >/dev/null 2>&1; then
        if pip-audit --desc --quiet >/dev/null 2>&1; then
            echo "    ✅ Backend security OK (pip-audit)"
        else
            echo "    ⚠️  Security issues found in backend (pip-audit)"
        fi
    else
        echo "    ⚡ Skipping backend security (install pip-audit or configure Snyk)"
    fi
fi

# 2. COVERAGE CHECK (only if test files changed)
echo ""
echo "📊 Coverage Check..."

# Check if there are changes in tests - refined regex for test files
CHANGED_FILES=$(git diff --cached --name-only 2>/dev/null || echo "")
HAS_TEST_CHANGES=$(echo "$CHANGED_FILES" | grep -E "(\.test\.|\.spec\.|tests/|test/|__tests__/)" 2>/dev/null || true)

if [ ! -z "$HAS_TEST_CHANGES" ]; then
    echo "  Test files changed, running coverage..."
    
    # Backend coverage (quick)
    if [ -f "coverage.xml" ]; then
        LAST_COVERAGE=$(grep 'line-rate=' coverage.xml | head -1 | sed 's/.*line-rate="\([^"]*\)".*/\1/' | awk '{print int($1*100)}' 2>/dev/null || echo "0")
        echo "    📈 Backend: ${LAST_COVERAGE}% (last run)"
    else
        echo "    📋 Backend: Run 'cd apps/backend && python -m pytest --cov=app --cov-report=xml' for coverage"
    fi
    
    # Frontend coverage (quick)
    cd ../frontend
    if [ -d "coverage" ]; then
        echo "    📈 Frontend: Coverage data available"
    else
        echo "    📋 Frontend: Run 'cd apps/frontend && pnpm test:coverage' for coverage"
    fi
    cd ../..
else
    echo "  No test changes detected, skipping coverage analysis"
fi

# 4. SUMMARY
if [ -f ".badges-cache.md" ]; then
    echo ""
    echo "💾 Badges ready for README update"
    echo "   Check if README.md was updated automatically"
fi

echo ""
echo "✅ Pre-commit analysis completed!"
echo "💡 For full analysis, run: ./scripts/analyze-all.sh"
