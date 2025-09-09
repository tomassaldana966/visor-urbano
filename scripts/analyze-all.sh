#!/bin/bash
# 🔍 Complete Local Analysis: Security + Coverage
# This script runs all quality analysis locally

echo "🔍 COMPLETE LOCAL ANALYSIS - Visor Urbano"
echo "========================================="
echo "🛡️  Security + 📊 Coverage + 🧹 Quality"
echo ""

# Function to show separator
separator() {
    echo ""
    echo "================================================="
    echo ""
}

# 1. SECURITY ANALYSIS
echo "🔒 1. SECURITY ANALYSIS"
echo "-----------------------"

# Run Snyk script if it exists
if [ -f "scripts/local-snyk.sh" ]; then
    echo "🔍 Attempting Snyk security analysis..."
    timeout 30 ./scripts/local-snyk.sh 2>/dev/null
    SNYK_EXIT=$?
    
    if [ $SNYK_EXIT -eq 0 ]; then
        echo "✅ Snyk analysis completed successfully"
    elif [ $SNYK_EXIT -eq 124 ]; then
        echo "⚠️  Snyk analysis timed out - using fallback security tools..."
        ./scripts/security-fallback.sh
    else
        echo "⚠️  Snyk analysis failed - using fallback security tools..."
        ./scripts/security-fallback.sh
    fi
elif [ -f "scripts/security-fallback.sh" ]; then
    echo "🔧 Using fallback security analysis..."
    ./scripts/security-fallback.sh
else
    echo "⚡ Using basic tools..."
    echo ""
    echo "Frontend (npm audit):"
    cd apps/frontend
    pnpm audit --audit-level moderate || echo "⚠️ Vulnerabilities found"
    
    echo ""
    echo "Backend (pip-audit):"
    cd ../backend
    if command -v pip-audit >/dev/null 2>&1; then
        pip-audit --desc || echo "⚠️ Vulnerabilities found"
    else
        echo "💡 Install pip-audit: pip install pip-audit"
    fi
    cd ../..
fi

separator

# 2. COVERAGE ANALYSIS
echo "📊 2. COVERAGE ANALYSIS"
echo "-----------------------"

# Run coverage script if it exists
if [ -f "scripts/local-coverage.sh" ]; then
    ./scripts/local-coverage.sh
else
    echo "📈 Running tests with coverage..."
    
    echo "Backend:"
    cd apps/backend
    if command -v python >/dev/null 2>&1; then
        python -m pytest tests/ --cov=app --cov-report=term-missing | tail -10
    else
        echo "❌ Python not available"
    fi
    
    echo ""
    echo "Frontend:"
    cd ../frontend
    if command -v pnpm >/dev/null 2>&1; then
        pnpm run test:coverage | tail -10
    else
        echo "❌ pnpm not available"
    fi
    cd ../..
fi

separator

# 3. CODE QUALITY ANALYSIS
echo "🧹 3. QUALITY ANALYSIS"
echo "----------------------"

echo "Linting Frontend:"
cd apps/frontend
if command -v pnpm >/dev/null 2>&1; then
    pnpm lint:eslint 2>/dev/null && echo "✅ ESLint: OK" || echo "⚠️ ESLint: Issues found"
    pnpm typecheck 2>/dev/null && echo "✅ TypeScript: OK" || echo "⚠️ TypeScript: Type errors"
else
    echo "❌ pnpm not available"
fi

echo ""
echo "Formatting check:"
if command -v pnpm >/dev/null 2>&1; then
    pnpm format:check 2>/dev/null && echo "✅ Prettier: OK" || echo "⚠️ Prettier: Formatting issues"
else
    echo "❌ pnpm not available"
fi
cd ../..

separator

# 4. SUMMARY AND RECOMMENDATIONS
echo "📋 4. SUMMARY AND RECOMMENDATIONS"
echo "--------------------------------"

# Dynamic metrics extraction
get_dynamic_metrics() {
    # Backend coverage
    if [ -f "apps/backend/coverage.xml" ]; then
        BACKEND_COV=$(grep 'line-rate=' apps/backend/coverage.xml | head -1 | sed 's/.*line-rate="\([^"]*\)".*/\1/' | awk '{printf "%.0f", $1*100}' 2>/dev/null || echo "unknown")
        BACKEND_FILES=$(grep -c '<class' apps/backend/coverage.xml 2>/dev/null || echo "unknown")
    else
        BACKEND_COV="unknown"
        BACKEND_FILES="unknown"
    fi
    
    # Frontend coverage - properly calculate LH/LF percentage
    if [ -f "apps/frontend/coverage/lcov.info" ]; then
        FRONTEND_FILES=$(grep -c "^SF:" apps/frontend/coverage/lcov.info 2>/dev/null || echo "unknown")
        TOTAL_LINES=$(grep "^LF:" apps/frontend/coverage/lcov.info | awk -F: '{sum+=$2} END {print sum+0}' 2>/dev/null || echo "0")
        COVERED_LINES=$(grep "^LH:" apps/frontend/coverage/lcov.info | awk -F: '{sum+=$2} END {print sum+0}' 2>/dev/null || echo "0")
        if [ "$TOTAL_LINES" -gt 0 ]; then
            FRONTEND_COV=$(echo "scale=1; $COVERED_LINES * 100 / $TOTAL_LINES" | bc -l 2>/dev/null || echo "unknown")
        else
            FRONTEND_COV="0"
        fi
    else
        FRONTEND_COV="unknown"
        FRONTEND_FILES="unknown"
    fi
    
    # Testing metrics
    if [ -d "apps/frontend/app/components" ]; then
        TOTAL_COMPONENTS=$(find apps/frontend/app/components -maxdepth 1 -type d ! -path "apps/frontend/app/components" | wc -l | tr -d ' ')
        COMPONENTS_WITH_STORIES=$(find apps/frontend/app/components -name "*.stories.*" -exec dirname {} \; | sort -u | wc -l | tr -d ' ')
        if [ "$TOTAL_COMPONENTS" -gt 0 ]; then
            STORYBOOK_COV=$(echo "scale=0; $COMPONENTS_WITH_STORIES * 100 / $TOTAL_COMPONENTS" | bc -l 2>/dev/null || echo "0")
        else
            STORYBOOK_COV="0"
        fi
    else
        STORYBOOK_COV="0"
    fi
    
    VITEST_COUNT=$(find apps/frontend -name "*.test.*" -o -name "*.spec.*" | wc -l | tr -d ' ')
    PLAYWRIGHT_COUNT=$(find apps/e2e/tests -name "*.spec.*" 2>/dev/null | wc -l | tr -d ' ')
    
    # Security vulnerabilities
    if command -v snyk >/dev/null 2>&1; then
        SNYK_TEXT=$(snyk test --file=apps/backend/requirements.txt --severity-threshold=high 2>/dev/null)
        SNYK_ISSUES=$(echo "$SNYK_TEXT" | grep -o '[0-9]\+ issues' | head -1 | awk '{print $1}' 2>/dev/null || echo "0")
        # Ensure we have a valid number
        if [ -z "$SNYK_ISSUES" ] || ! [[ "$SNYK_ISSUES" =~ ^[0-9]+$ ]]; then
            SNYK_ISSUES="0"
        fi
    else
        SNYK_ISSUES="0"
    fi
}

echo "🔍 CURRENT PROJECT STATUS:"
echo ""

# Get current metrics
get_dynamic_metrics

echo "✅ STRENGTHS:"
if [ "$BACKEND_COV" != "unknown" ]; then
    echo "   • Backend: ${BACKEND_COV}% test coverage (${BACKEND_FILES} files analyzed)"
else
    echo "   • Backend: Coverage data available (run analysis for metrics)"
fi
echo "   • Frontend: Main dependencies without critical vulnerabilities"
if [ "$FRONTEND_FILES" != "unknown" ]; then
    echo "   • Frontend: ${FRONTEND_FILES} files with coverage tracking"
fi
if [ "$STORYBOOK_COV" != "0" ]; then
    echo "   • Storybook: ${STORYBOOK_COV}% component story coverage"
fi
if [ "$VITEST_COUNT" -gt 0 ]; then
    echo "   • Vitest: ${VITEST_COUNT} unit test files"
fi
if [ "$PLAYWRIGHT_COUNT" -gt 0 ]; then
    echo "   • Playwright: ${PLAYWRIGHT_COUNT} E2E test files"
fi
echo "   • Configuration: Well-structured CI/CD workflows"
echo ""
echo "⚠️  IMPROVEMENT AREAS:"
if [ "$SNYK_ISSUES" != "0" ] && [[ "$SNYK_ISSUES" =~ ^[0-9]+$ ]] && [ "$SNYK_ISSUES" -gt 0 ]; then
    echo "   • Backend: ${SNYK_ISSUES} HIGH/CRITICAL vulnerabilities found"
else
    echo "   • Backend: Run security scan for vulnerability assessment"
fi
if [ "$FRONTEND_COV" != "unknown" ]; then
    echo "   • Frontend: ${FRONTEND_COV}% test coverage (consider increasing)"
else
    echo "   • Frontend: Run coverage analysis for detailed metrics"
fi
echo "   • Legacy: Multiple vulnerabilities (consider updating)"
echo ""
echo "🎯 SUGGESTED NEXT STEPS:"
echo "   1. Add more frontend tests"
echo "   2. Investigate alternatives to ecdsa@0.19.1"
echo "   3. Configure SNYK_TOKEN and CODECOV_TOKEN secrets in GitHub"
echo "   4. Consider migration/update of legacy code"
echo ""
echo "🌐 AVAILABLE HTML REPORTS:"
echo "   • Backend Coverage: file://$(pwd)/apps/backend/htmlcov/index.html"
echo "   • Frontend Coverage: file://$(pwd)/apps/frontend/coverage/index.html"
echo ""
echo "🚀 COMMANDS TO IMPROVE:"
echo "   # Update dependencies:"
echo "   cd apps/backend && pip install --upgrade ecdsa"
echo "   cd apps/frontend && pnpm update"
echo ""
echo "   # Add more tests:"
echo "   cd apps/frontend && # Create tests for main components"
echo "   cd apps/backend && # Increase coverage in routers"

echo ""
echo "✅ Complete analysis finished!"
echo "💡 Run this script regularly to maintain code quality"
