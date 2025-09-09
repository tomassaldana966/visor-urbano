#!/bin/bash
# 🏠 Local Coverage Analysis Script
# This script simulates what Codecov does locally

echo "🔍 Analyzing local coverage for Visor Urbano..."
echo "==============================================="

# Functions to extract dynamic metrics
get_backend_coverage() {
    local coverage_file="apps/backend/coverage.xml"
    if [ -f "$coverage_file" ]; then
        if command -v xmllint >/dev/null 2>&1; then
            local rate=$(xmllint --xpath "string(//coverage/@line-rate)" "$coverage_file" 2>/dev/null)
            if [ ! -z "$rate" ]; then
                echo "$rate * 100" | bc -l | xargs printf "%.2f"
            else
                echo "0"
            fi
        else
            # Fallback: parse XML manually
            grep 'line-rate=' "$coverage_file" | head -1 | sed 's/.*line-rate="\([^"]*\)".*/\1/' | awk '{printf "%.2f", $1*100}'
        fi
    else
        echo "0"
    fi
}

get_backend_test_count() {
    local coverage_file="apps/backend/coverage.xml"
    if [ -f "$coverage_file" ]; then
        # Count number of test files or classes in coverage
        if command -v xmllint >/dev/null 2>&1; then
            xmllint --xpath "count(//class)" "$coverage_file" 2>/dev/null || echo "0"
        else
            grep -c '<class' "$coverage_file" 2>/dev/null || echo "0"
        fi
    else
        echo "0"
    fi
}

get_frontend_file_count() {
    local coverage_file="apps/frontend/coverage/lcov.info"
    if [ -f "$coverage_file" ]; then
        grep -c "^SF:" "$coverage_file" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

get_frontend_coverage() {
    local coverage_file="apps/frontend/coverage/lcov.info"
    if [ -f "$coverage_file" ]; then
        local total_lines=$(grep "^LF:" "$coverage_file" | awk -F: '{sum+=$2} END {print sum+0}')
        local covered_lines=$(grep "^LH:" "$coverage_file" | awk -F: '{sum+=$2} END {print sum+0}')
        
        if [ "$total_lines" -gt 0 ]; then
            echo "scale=2; $covered_lines * 100 / $total_lines" | bc -l 2>/dev/null || echo "0"
        else
            echo "0"
        fi
    else
        echo "0"
    fi
}

# Check if coverage files exist
BACKEND_COVERAGE="apps/backend/coverage.xml"
FRONTEND_COVERAGE="apps/frontend/coverage/lcov.info"

echo ""
echo "📊 BACKEND COVERAGE (Python)"
echo "----------------------------"
if [ -f "$BACKEND_COVERAGE" ]; then
    echo "✅ XML file found: $BACKEND_COVERAGE"
    
    # Get dynamic coverage percentage
    COVERAGE_PERCENT=$(get_backend_coverage)
    TEST_COUNT=$(get_backend_test_count)
    
    echo "📈 Line coverage: ${COVERAGE_PERCENT}%"
    echo "🧪 Files in coverage: ${TEST_COUNT}"
    
    # Show files with lower coverage
    echo ""
    echo "📋 Files with lower coverage (last 10):"
    if command -v xmllint >/dev/null 2>&1; then
        xmllint --xpath "//class/@filename" "$BACKEND_COVERAGE" 2>/dev/null | \
        sed 's/filename="//g' | sed 's/"//g' | \
        head -10 | sed 's/^/   - /'
    fi
else
    echo "❌ coverage.xml not found. Run first:"
    echo "   cd apps/backend && python -m pytest tests/ --cov=app --cov-report=xml"
fi

echo ""
echo "📊 FRONTEND COVERAGE (TypeScript)"
echo "--------------------------------"
if [ -f "$FRONTEND_COVERAGE" ]; then
    echo "✅ LCOV file found: $FRONTEND_COVERAGE"
    
    # Extract statistics from LCOV - LH (lines hit) / LF (lines found) * 100
    FILE_COUNT=$(get_frontend_file_count)
    TOTAL_LINES=$(grep "^LF:" "$FRONTEND_COVERAGE" | awk -F: '{sum+=$2} END {print sum+0}')
    COVERED_LINES=$(grep "^LH:" "$FRONTEND_COVERAGE" | awk -F: '{sum+=$2} END {print sum+0}')
    FRONTEND_PERCENT=$(get_frontend_coverage)
    
    echo "📁 Files with coverage: $FILE_COUNT"
    echo "📊 Lines found: $TOTAL_LINES | Lines hit: $COVERED_LINES"
    echo "📈 Line coverage: ${FRONTEND_PERCENT}%"
else
    echo "❌ lcov.info not found. Run first:"
    echo "   cd apps/frontend && pnpm run test:coverage"
fi

echo ""
echo "🌐 LOCAL HTML REPORTS"
echo "---------------------"
echo "📂 Backend:  file://$(pwd)/apps/backend/htmlcov/index.html"
echo "📂 Frontend: file://$(pwd)/apps/frontend/coverage/index.html"

echo ""
echo "🚀 USEFUL COMMANDS"
echo "------------------"
echo "# Generate complete coverage:"
echo "cd apps/backend && python -m pytest tests/ --cov=app --cov-report=html --cov-report=xml --cov-report=term"
echo "cd apps/frontend && pnpm run test:coverage"
echo ""
echo "# View coverage in terminal only:"
echo "cd apps/backend && python -m pytest tests/ --cov=app --cov-report=term-missing"
echo "cd apps/frontend && pnpm run test:coverage --reporter=text"

echo ""
echo "💡 TIPS"
echo "-------"
echo "• XML/LCOV files are uploaded to Codecov"
echo "• HTML reports are for detailed local navigation"
echo "• Codecov combines both reports automatically"
echo "• Set thresholds in codecov.yml for quality control"
echo "• Create more Storybook stories to improve component coverage"
echo "• Add unit tests (.test.ts/.spec.ts) to improve Vitest coverage"
echo "• Add E2E tests in apps/e2e/tests/ to improve Playwright coverage"

echo ""
echo "✅ Analysis completed!"

echo ""
echo "🧪 TESTING COVERAGE METRICS"
echo "---------------------------"

# Storybook Coverage
COMPONENTS_DIR="apps/frontend/app/components"
if [ -d "$COMPONENTS_DIR" ]; then
    TOTAL_COMPONENTS=$(find "$COMPONENTS_DIR" -maxdepth 1 -type d ! -path "$COMPONENTS_DIR" | wc -l | tr -d ' ')
    COMPONENTS_WITH_STORIES=$(find "$COMPONENTS_DIR" -name "*.stories.*" -exec dirname {} \; | sort -u | wc -l | tr -d ' ')
    if [ "$TOTAL_COMPONENTS" -gt 0 ]; then
        STORYBOOK_PERCENT=$(echo "scale=1; $COMPONENTS_WITH_STORIES * 100 / $TOTAL_COMPONENTS" | bc -l 2>/dev/null || echo "0")
        echo "📚 Storybook: ${COMPONENTS_WITH_STORIES}/${TOTAL_COMPONENTS} components (${STORYBOOK_PERCENT}%)"
    else
        echo "📚 Storybook: No components found"
    fi
else
    echo "📚 Storybook: Components directory not found"
fi

# Vitest Coverage
VITEST_TESTS=$(find apps/frontend -name "*.test.*" -o -name "*.spec.*" | wc -l | tr -d ' ')
echo "🧪 Vitest: ${VITEST_TESTS} test files"

# Playwright Coverage
if [ -d "apps/e2e/tests" ]; then
    PLAYWRIGHT_TESTS=$(find apps/e2e/tests -name "*.spec.*" | wc -l | tr -d ' ')
    echo "🎭 Playwright: ${PLAYWRIGHT_TESTS} E2E test files"
else
    echo "🎭 Playwright: No E2E tests directory found"
fi
