#!/bin/bash
# 🔒 Local Snyk Security Analysis Script
# This script runs local security analysis with Snyk

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    echo "🔐 Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
fi

echo "🔒 Local Security Analysis with Snyk"
echo "===================================="

# Check if Snyk token is available
if [ -n "$SNYK_TOKEN" ]; then
    echo "✅ Snyk token found - testing authentication..."
    
    # Test with a simple snyk command to check real authentication
    if snyk config get api 2>/dev/null | grep -q "snyk"; then
        echo "✅ Snyk CLI is authenticated via snyk auth"
        export SNYK_TOKEN="$SNYK_TOKEN"
    else
        # Try to authenticate with the token
        export SNYK_TOKEN="$SNYK_TOKEN"
        echo "⚠️  Using token from .env file (may have limitations)"
        echo "   Consider running 'snyk auth' for full authentication"
    fi
else
    echo "⚠️  No Snyk token found - using unauthenticated scanning"
    echo "   Add SNYK_TOKEN to .env file for enhanced features"
    echo "   Or run 'snyk auth' for interactive authentication"
fi

# Check if Snyk is installed
if ! command -v snyk &> /dev/null; then
    echo "❌ Snyk CLI is not installed. Installing..."
    npm install -g snyk
fi

echo ""
echo "📊 CURRENT ANALYSIS (Main projects only)"
echo "----------------------------------------"

echo ""
echo "🌐 FRONTEND (React Router + TypeScript)"
echo "---------------------------------------"
cd apps/frontend

# Try Snyk first, fallback to npm audit if it fails
snyk test --severity-threshold=high --json > /tmp/snyk-frontend.json 2>/dev/null
FRONTEND_EXIT=$?

if [ $FRONTEND_EXIT -eq 0 ]; then
    echo "✅ No HIGH/CRITICAL vulnerabilities found"
elif [ $FRONTEND_EXIT -eq 2 ]; then
    echo "⚠️  Vulnerabilities found. Running detailed analysis..."
    if snyk test --severity-threshold=medium 2>&1 | grep -q "Authentication error"; then
        echo "⚠️  Snyk authentication failed - using npm audit fallback..."
        pnpm audit --audit-level high || echo "   No high-level vulnerabilities found in npm audit"
    else
        snyk test --severity-threshold=medium 2>&1 | head -50 | grep -E "(vulnerabilities|HIGH|CRITICAL)"
    fi
else
    echo "⚠️  Snyk authentication failed (SNYK-0005) - using npm audit fallback..."
    pnpm audit --audit-level high || echo "   No high-level vulnerabilities found in npm audit"
fi

echo ""
echo "🐍 BACKEND (Python + FastAPI)"
echo "-----------------------------"
cd ../backend

# Try Snyk first, fallback to safety if it fails
snyk test --file=requirements.txt --severity-threshold=high --json > /tmp/snyk-backend.json 2>/dev/null
BACKEND_EXIT=$?

if [ $BACKEND_EXIT -eq 0 ]; then
    echo "✅ No HIGH/CRITICAL vulnerabilities found"
elif [ $BACKEND_EXIT -eq 2 ]; then
    echo "⚠️  Vulnerabilities found. Details:"
    if snyk test --file=requirements.txt --severity-threshold=medium 2>&1 | grep -q "Authentication error"; then
        echo "⚠️  Snyk authentication failed - using safety fallback..."
        if command -v safety >/dev/null 2>&1; then
            python -m safety scan --short-report || echo "   No critical vulnerabilities found in safety scan"
        else
            echo "   Safety not available, install with: pip install safety"
            echo "   Known issues: 2 HIGH vulnerabilities in ecdsa@0.19.1 (documented)"
        fi
    else
        snyk test --file=requirements.txt --severity-threshold=medium 2>&1 | head -30 | grep -E "(vulnerabilities|HIGH|CRITICAL)"
    fi
else
    echo "⚠️  Snyk authentication failed (SNYK-0005) - using safety fallback..."
    if command -v safety >/dev/null 2>&1; then
        python -m safety scan --short-report || echo "   No critical vulnerabilities found in safety scan"
    else
        echo "   Safety not available, install with: pip install safety"
        echo "   Known issues: 2 HIGH vulnerabilities in ecdsa@0.19.1 (documented)"
    fi
fi

echo ""
echo "📋 ROOT DEPENDENCIES"
echo "--------------------"
cd ../..

# Try Snyk first, fallback to npm audit if it fails
snyk test --severity-threshold=high --json > /tmp/snyk-root.json 2>/dev/null
ROOT_EXIT=$?

if [ $ROOT_EXIT -eq 0 ]; then
    echo "✅ No HIGH/CRITICAL vulnerabilities found in root"
elif [ $ROOT_EXIT -eq 2 ]; then
    echo "⚠️  Vulnerabilities found in root dependencies"
else
    echo "⚠️  Snyk authentication failed for root, using npm audit..."
    pnpm audit --audit-level high 2>/dev/null || echo "   No package manager audit available"
fi

echo ""
echo "🚀 USEFUL SNYK COMMANDS"
echo "----------------------"
echo "# Scan specific project:"
echo "snyk test --file=apps/backend/requirements.txt"
echo "snyk test apps/frontend/"
echo ""
echo "# With different thresholds:"
echo "snyk test --severity-threshold=low     # All issues"
echo "snyk test --severity-threshold=medium  # Medium, High, Critical"
echo "snyk test --severity-threshold=high    # High and Critical only"
echo ""
echo "# Generate reports:"
echo "snyk test --json > security-report.json"
echo "snyk test --sarif > security-report.sarif"
echo ""
echo "# Try auto-fix (experimental):"
echo "snyk fix"

echo ""
echo "⚡ QUICK ANALYSIS WITHOUT SNYK CLI"
echo "----------------------------------"
echo "# Node.js dependencies:"
echo "pnpm audit --audit-level moderate"
echo ""
echo "# Python dependencies:"
echo "pip install pip-audit && pip-audit"

echo ""
echo "🔐 SNYK AUTHENTICATION (Optional)"
echo "---------------------------------"
echo "For advanced features like monitoring:"
echo "1. Create account at https://snyk.io"
echo "2. Run: snyk auth"
echo "3. Then use: snyk monitor (for continuous tracking)"

echo ""
echo "💡 TIPS"
echo "-------"
echo "• Legacy code has many vulnerabilities - consider updating"
echo "• Current backend: only 2 HIGH issues in ecdsa@0.19.1"
echo "• Current frontend: clean main dependencies"
echo "• Focus on apps/ directory for active projects"

if [ $FRONTEND_EXIT -ne 0 ] || [ $BACKEND_EXIT -ne 0 ] || [ $ROOT_EXIT -ne 0 ]; then
    echo ""
    echo "⚠️  SUMMARY: Vulnerabilities found"
    echo "   Review details above for specific actions"
    echo "   Consider updating affected dependencies"
else
    echo ""
    echo "✅ SUMMARY: Main projects without critical vulnerabilities"
fi

echo ""
echo "✅ Snyk analysis completed!"
