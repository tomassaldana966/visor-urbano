#!/bin/bash
# 🏷️ Dynamic Badge Updater
# Updates badges in README.md based on current analysis
# Supports smart updating only when significant changes occur

# Parse command line arguments
AUTO_UPDATE=false
SMART_UPDATE=false
FORCE_UPDATE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --auto-update)
            AUTO_UPDATE=true
            shift
            ;;
        --smart-update)
            SMART_UPDATE=true
            shift
            ;;
        --force-update)
            FORCE_UPDATE=true
            shift
            ;;
        --apply)
            AUTO_UPDATE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--auto-update|--smart-update|--force-update|--apply]"
            exit 1
            ;;
    esac
done

echo "🏷️ Updating README badges..."

# Functions to detect significant changes
get_current_metrics_from_readme() {
    if [ -f "README.md" ]; then
        # Extract current metrics from README badges
        CURRENT_BACKEND=$(grep "backend%20coverage" README.md | sed 's/.*coverage-\([0-9]*\)%25.*/\1/' || echo "0")
        CURRENT_FRONTEND=$(grep "frontend%20coverage" README.md | sed 's/.*coverage-\([^%]*\)%25.*/\1/' || echo "0")
        CURRENT_STORYBOOK=$(grep "storybook%20coverage" README.md | sed 's/.*coverage-\([0-9]*\)%25.*/\1/' || echo "0")
        CURRENT_SNYK=$(grep "snyk-" README.md | sed 's/.*snyk-\([0-9]*\)%20known%20issues.*/\1/' || echo "0")
        CURRENT_VITEST=$(grep "vitest%20tests" README.md | sed 's/.*tests-\([0-9]*\)%20files.*/\1/' || echo "0")
        CURRENT_PLAYWRIGHT=$(grep "playwright%20e2e" README.md | sed 's/.*e2e-\([0-9]*\)%20tests.*/\1/' || echo "0")
    else
        CURRENT_BACKEND="0"
        CURRENT_FRONTEND="0" 
        CURRENT_STORYBOOK="0"
        CURRENT_SNYK="0"
        CURRENT_VITEST="0"
        CURRENT_PLAYWRIGHT="0"
    fi
}

check_significant_changes() {
    get_current_metrics_from_readme
    
    # Define thresholds for significant changes
    # Calculate the absolute difference for backend coverage
    local backend_diff=$(echo "$BACKEND_COVERAGE - $CURRENT_BACKEND" | bc -l 2>/dev/null)
    backend_diff=${backend_diff#-}  # Remove negative sign to get absolute value
    
    # Calculate the absolute difference for frontend coverage
    local frontend_diff=$(echo "$FRONTEND_COVERAGE - $CURRENT_FRONTEND" | bc -l 2>/dev/null)
    frontend_diff=${frontend_diff#-}  # Remove negative sign to get absolute value
    
    # Calculate the absolute difference for storybook coverage
    local storybook_diff=$(echo "$STORYBOOK_COVERAGE - $CURRENT_STORYBOOK" | bc -l 2>/dev/null)
    storybook_diff=${storybook_diff#-}  # Remove negative sign to get absolute value
    
    # Calculate the absolute difference for Snyk issues
    local snyk_diff=$(echo "$SNYK_ISSUES - $CURRENT_SNYK" | bc -l 2>/dev/null)
    snyk_diff=${snyk_diff#-}  # Remove negative sign to get absolute value
    
    # Calculate the absolute difference for Vitest tests
    local vitest_diff=$(echo "$VITEST_TESTS - $CURRENT_VITEST" | bc -l 2>/dev/null)
    vitest_diff=${vitest_diff#-}  # Remove negative sign to get absolute value
    
    # Calculate the absolute difference for Playwright tests
    local playwright_diff=$(echo "$PLAYWRIGHT_TESTS - $CURRENT_PLAYWRIGHT" | bc -l 2>/dev/null)
    playwright_diff=${playwright_diff#-}  # Remove negative sign to get absolute value
    
    # Check for significant changes (adjust thresholds as needed)
    if (( $(echo "$backend_diff >= 5" | bc -l) )) || \
       (( $(echo "$frontend_diff >= 1" | bc -l) )) || \
       (( $(echo "$storybook_diff >= 10" | bc -l) )) || \
       (( $(echo "$snyk_diff >= 1" | bc -l) )) || \
       (( $(echo "$vitest_diff >= 2" | bc -l) )) || \
       (( $(echo "$playwright_diff >= 1" | bc -l) )); then
        return 0  # Significant changes found
    else
        return 1  # No significant changes
    fi
}

update_readme_badges() {
    local temp_file="README_temp.md"
    
    # Create a temporary file with updated badges
    awk '
    BEGIN { in_badges = 0; badges_replaced = 0 }
    /^# Visor Urbano$/ { 
        print $0
        in_badges = 1
        next 
    }
    in_badges && /^\[/ && /badge/ { 
        if (!badges_replaced) {
            # Insert new badges from file
            while ((getline line < ".badges-cache.md") > 0) {
                print line
            }
            close(".badges-cache.md")
            badges_replaced = 1
        }
        next
    }
    in_badges && !/^\[/ && !/^$/ { 
        in_badges = 0
        print ""
        print $0
        next
    }
    in_badges && /^$/ { next }
    !in_badges { print $0 }
    ' README.md > "$temp_file"
    
    # Replace original file if update was successful
    if [ -f "$temp_file" ] && [ -s "$temp_file" ]; then
        mv "$temp_file" README.md
        echo "✅ README.md updated successfully"
        return 0
    else
        echo "❌ Failed to update README.md"
        rm -f "$temp_file"
        return 1
    fi
}

# Run quick analysis

# Get current metrics dynamically
echo "📊 Gathering metrics..."

# Function to calculate Storybook coverage
get_storybook_coverage() {
    local components_dir="apps/frontend/app/components"
    if [ -d "$components_dir" ]; then
        # Count component directories (excluding the parent directory itself)
        local total_components=$(find "$components_dir" -maxdepth 1 -type d ! -path "$components_dir" | wc -l | tr -d ' ')
        # Count unique component directories that have stories
        local components_with_stories=$(find "$components_dir" -name "*.stories.*" -exec dirname {} \; | sort -u | wc -l | tr -d ' ')
        
        if [ "$total_components" -gt 0 ]; then
            echo "scale=0; $components_with_stories * 100 / $total_components" | bc -l 2>/dev/null || echo "0"
        else
            echo "0"
        fi
    else
        echo "0"
    fi
}

# Function to get Vitest test count
get_vitest_metrics() {
    local frontend_dir="apps/frontend"
    if [ -d "$frontend_dir" ]; then
        # Count .test.* and .spec.* files
        local test_files=$(find "$frontend_dir" -name "*.test.*" -o -name "*.spec.*" | wc -l | tr -d ' ')
        echo "$test_files"
    else
        echo "0"
    fi
}

# Function to get Playwright test count  
get_playwright_metrics() {
    local e2e_dir="apps/e2e/tests"
    if [ -d "$e2e_dir" ]; then
        local e2e_tests=$(find "$e2e_dir" -name "*.spec.*" | wc -l | tr -d ' ')
        echo "$e2e_tests"
    else
        echo "0"
    fi
}

# Backend Coverage - improved extraction
if [ -f "apps/backend/coverage.xml" ]; then
    if command -v xmllint >/dev/null 2>&1; then
        BACKEND_COVERAGE=$(xmllint --xpath "string(//coverage/@line-rate)" apps/backend/coverage.xml 2>/dev/null | awk '{printf "%.0f", $1*100}')
    else
        BACKEND_COVERAGE=$(grep 'line-rate=' apps/backend/coverage.xml | head -1 | sed 's/.*line-rate="\([^"]*\)".*/\1/' | awk '{printf "%.0f", $1*100}')
    fi
    
    # Fallback if extraction fails
    if [ -z "$BACKEND_COVERAGE" ] || [ "$BACKEND_COVERAGE" = "0" ]; then
        BACKEND_COVERAGE="unknown"
        BACKEND_COLOR="lightgrey"
    elif [ "$BACKEND_COVERAGE" -gt 80 ]; then
        BACKEND_COLOR="brightgreen"
    elif [ "$BACKEND_COVERAGE" -gt 60 ]; then
        BACKEND_COLOR="yellow"
    else
        BACKEND_COLOR="red"
    fi
else
    BACKEND_COVERAGE="no%20data"
    BACKEND_COLOR="lightgrey"
fi

# Frontend Coverage - improved extraction using LH/LF calculation
if [ -f "apps/frontend/coverage/lcov.info" ]; then
    TOTAL_LINES=$(grep "^LF:" apps/frontend/coverage/lcov.info | awk -F: '{sum+=$2} END {print sum+0}' 2>/dev/null || echo "0")
    COVERED_LINES=$(grep "^LH:" apps/frontend/coverage/lcov.info | awk -F: '{sum+=$2} END {print sum+0}' 2>/dev/null || echo "0")
    
    if [ "$TOTAL_LINES" -gt 0 ]; then
        FRONTEND_COVERAGE=$(echo "scale=1; $COVERED_LINES * 100 / $TOTAL_LINES" | bc -l 2>/dev/null || echo "0")
        FRONTEND_STATUS="${FRONTEND_COVERAGE}%25"
        # Set color based on coverage percentage
        if (( $(echo "$FRONTEND_COVERAGE > 80" | bc -l) )); then
            FRONTEND_COLOR="brightgreen"
        elif (( $(echo "$FRONTEND_COVERAGE > 60" | bc -l) )); then
            FRONTEND_COLOR="yellow"
        else
            FRONTEND_COLOR="red"
        fi
    else
        FRONTEND_STATUS="no%20data"
        FRONTEND_COLOR="lightgrey"
        FRONTEND_COVERAGE="0"
    fi
else
    # Try to get actual test count from package.json test scripts if coverage file doesn't exist
    if command -v pnpm >/dev/null 2>&1; then
        cd apps/frontend >/dev/null 2>&1
        FRONTEND_TESTS=$(pnpm test:vitest --reporter=json 2>/dev/null | jq '.numPassedTests // 0' 2>/dev/null || echo "0")
        cd - >/dev/null 2>&1
        if [ "$FRONTEND_TESTS" -gt 0 ]; then
            FRONTEND_STATUS="${FRONTEND_TESTS}%20passing"
            FRONTEND_COLOR="blue"
        else
            FRONTEND_STATUS="no%20data"
            FRONTEND_COLOR="lightgrey"
        fi
    else
        FRONTEND_STATUS="no%20data"
        FRONTEND_COLOR="lightgrey"
    fi
fi

# Security Status - improved vulnerability detection
SECURITY_STATUS="analyzed"
if command -v snyk >/dev/null 2>&1; then
    # Try to get actual vulnerability count
    SNYK_OUTPUT=$(snyk test --file=apps/backend/requirements.txt --severity-threshold=high --json 2>/dev/null)
    if [ $? -eq 0 ]; then
        SNYK_ISSUES=$(echo "$SNYK_OUTPUT" | jq '.vulnerabilities | length' 2>/dev/null || echo "0")
    else
        # If snyk fails, try parsing text output
        SNYK_TEXT=$(snyk test --file=apps/backend/requirements.txt --severity-threshold=high 2>/dev/null)
        SNYK_ISSUES=$(echo "$SNYK_TEXT" | grep -o '[0-9]\+ issues' | head -1 | awk '{print $1}' 2>/dev/null || echo "0")
        # If still no number, default to 0
        if [ -z "$SNYK_ISSUES" ] || ! [[ "$SNYK_ISSUES" =~ ^[0-9]+$ ]]; then
            SNYK_ISSUES="0"
        fi
    fi
    
    if [ "$SNYK_ISSUES" -gt 0 ]; then
        SECURITY_COLOR="orange"
        SNYK_STATUS="${SNYK_ISSUES}%20known%20issues"
    else
        SNYK_STATUS="no%20high%20issues"
        SECURITY_COLOR="brightgreen"
    fi
else
    SNYK_ISSUES="0"
    SNYK_STATUS="snyk%20not%20available"
    SECURITY_COLOR="lightgrey"
fi

# Version extraction - more robust
TS_VERSION=$(grep '"typescript"' apps/frontend/package.json | sed 's/.*"typescript": "\([^"]*\)".*/\1/' 2>/dev/null || echo "unknown")
PY_VERSION=$(python3 --version 2>/dev/null | cut -d' ' -f2 | cut -d'.' -f1,2 || echo "unknown")

# Testing metrics
STORYBOOK_COVERAGE=$(get_storybook_coverage)
VITEST_TESTS=$(get_vitest_metrics)
PLAYWRIGHT_TESTS=$(get_playwright_metrics)

# Set colors for testing badges
if [ "$STORYBOOK_COVERAGE" -gt 80 ]; then
    STORYBOOK_COLOR="brightgreen"
elif [ "$STORYBOOK_COVERAGE" -gt 60 ]; then
    STORYBOOK_COLOR="yellow"
else
    STORYBOOK_COLOR="red"
fi

if [ "$VITEST_TESTS" -gt 20 ]; then
    VITEST_COLOR="brightgreen"
elif [ "$VITEST_TESTS" -gt 5 ]; then
    VITEST_COLOR="yellow"
else
    VITEST_COLOR="red"
fi

if [ "$PLAYWRIGHT_TESTS" -gt 10 ]; then
    PLAYWRIGHT_COLOR="brightgreen"
elif [ "$PLAYWRIGHT_TESTS" -gt 3 ]; then
    PLAYWRIGHT_COLOR="yellow"
else
    PLAYWRIGHT_COLOR="red"
fi

echo "📈 Current metrics:"
echo "  Backend Coverage: ${BACKEND_COVERAGE}%"
echo "  Frontend Coverage: ${FRONTEND_COVERAGE}%"
echo "  Security Issues: ${SNYK_ISSUES}"
echo "  Storybook Coverage: ${STORYBOOK_COVERAGE}%"
echo "  Vitest Tests: ${VITEST_TESTS}"
echo "  Playwright Tests: ${PLAYWRIGHT_TESTS}"
echo "  TypeScript: ${TS_VERSION}"
echo "  Python: ${PY_VERSION}"

# Generate updated badges with dynamic values including testing tools
cat > .badges-cache.md << EOF
[![GitHub CI](https://github.com/Delivery-Associates/visor-urbano/actions/workflows/test.yml/badge.svg)](https://github.com/Delivery-Associates/visor-urbano/actions/workflows/test.yml)
[![Security Status](https://img.shields.io/badge/security-${SECURITY_STATUS}-${SECURITY_COLOR}?style=flat&logo=shield)](docs/SECURITY_COVERAGE_SETUP.md)
[![Backend Coverage](https://img.shields.io/badge/backend%20coverage-${BACKEND_COVERAGE}%25-${BACKEND_COLOR}?style=flat&logo=python)](apps/backend/htmlcov/index.html)
[![Frontend Coverage](https://img.shields.io/badge/frontend%20coverage-${FRONTEND_STATUS}-${FRONTEND_COLOR}?style=flat&logo=typescript)](apps/frontend/coverage/index.html)
[![Storybook Coverage](https://img.shields.io/badge/storybook%20coverage-${STORYBOOK_COVERAGE}%25-${STORYBOOK_COLOR}?style=flat&logo=storybook)](http://localhost:6006)
[![Vitest Tests](https://img.shields.io/badge/vitest%20tests-${VITEST_TESTS}%20files-${VITEST_COLOR}?style=flat&logo=vitest)](apps/frontend/coverage/index.html)
[![Playwright E2E](https://img.shields.io/badge/playwright%20e2e-${PLAYWRIGHT_TESTS}%20tests-${PLAYWRIGHT_COLOR}?style=flat&logo=playwright)](apps/e2e/tests)
[![Code Quality](https://img.shields.io/badge/code%20quality-monitored-blue?style=flat&logo=codacy)](scripts/analyze-all.sh)
[![Snyk Vulnerabilities](https://img.shields.io/badge/snyk-${SNYK_STATUS}-${SECURITY_COLOR}?style=flat&logo=snyk)](scripts/local-snyk.sh)
[![TypeScript](https://img.shields.io/badge/typescript-${TS_VERSION}-blue?style=flat&logo=typescript)](apps/frontend/tsconfig.json)
[![Python](https://img.shields.io/badge/python-${PY_VERSION}-blue?style=flat&logo=python)](apps/backend/requirements.txt)
EOF

# Copy badges to cache file for consistent access
cp .badges-cache.md .badges-cache.md

echo ""
echo "🏷️ Updated badges:"
echo "=================="
cat .badges-temp.md

# Smart update logic
if [ "$SMART_UPDATE" = true ]; then
    echo ""
    echo "• Checking for significant changes..."
    
    if check_significant_changes; then
        echo "📊 Significant changes detected:"
        echo "   Current -> New"
        echo "   Backend Coverage: ${CURRENT_BACKEND}% -> ${BACKEND_COVERAGE}%"
        echo "   Frontend Coverage: ${CURRENT_FRONTEND}% -> ${FRONTEND_COVERAGE}%"
        echo "   Storybook Coverage: ${CURRENT_STORYBOOK}% -> ${STORYBOOK_COVERAGE}%"
        echo "   Security Issues: ${CURRENT_SNYK} -> ${SNYK_ISSUES}"
        echo "   Vitest Tests: ${CURRENT_VITEST} -> ${VITEST_TESTS}"
        echo "   Playwright Tests: ${CURRENT_PLAYWRIGHT} -> ${PLAYWRIGHT_TESTS}"
        echo ""
        echo "🔄 Updating README.md automatically..."
        
        if update_readme_badges; then
            echo "✅ README.md updated with new metrics"
        else
            echo "❌ Failed to update README.md automatically"
        fi
    else
        echo "✅ No significant changes detected - README.md left unchanged"
        echo "💡 Thresholds: Backend ±5%, Frontend ±1%, Storybook ±10%, Security/Tests ±1"
    fi

elif [ "$AUTO_UPDATE" = true ] || [ "$FORCE_UPDATE" = true ]; then
    echo ""
    echo "🔄 Applying badges to README.md..."
    
    if update_readme_badges; then
        echo "✅ README.md updated successfully"
    else
        echo "❌ Failed to update README.md"
    fi

else
    echo ""
    echo "💡 To update README.md:"
    echo "   ./scripts/update-badges.sh --apply                (force update)"
    echo "   ./scripts/update-badges.sh --smart-update         (only if significant changes)"
    echo ""
    echo "💡 Badges cached in: .badges-cache.md"
fi

# Cleanup - keep cache file for use by other scripts

echo ""
echo "✅ Badge update completed!"
