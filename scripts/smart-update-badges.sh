#!/bin/bash
# 🏷️ Smart Badge Updater - Simplified Version
# Updates badges and README only when there are significant changes

# Parse command line arguments
SMART_UPDATE=false
AUTO_UPDATE=false

case "${1:-}" in
    --smart-update)
        SMART_UPDATE=true
        ;;
    --auto-update|--apply)
        AUTO_UPDATE=true
        ;;
    *)
        if [ -n "${1:-}" ]; then
            echo "Usage: $0 [--smart-update|--auto-update]"
            exit 1
        fi
        ;;
esac

echo "🏷️ Updating README badges..."

# Function to extract current metrics from README
get_current_readme_metrics() {
    if [ -f "README.md" ]; then
        CURRENT_BACKEND=$(grep "backend%20coverage" README.md | sed 's/.*coverage-\([0-9]*\)%25.*/\1/' 2>/dev/null || echo "0")
        CURRENT_SNYK=$(grep "snyk-" README.md | sed 's/.*snyk-\([0-9]*\)%20known%20issues.*/\1/' 2>/dev/null || echo "0")
        CURRENT_VITEST=$(grep "vitest%20tests" README.md | sed 's/.*tests-\([0-9]*\)%20files.*/\1/' 2>/dev/null || echo "0")
    else
        CURRENT_BACKEND="0"
        CURRENT_SNYK="0"
        CURRENT_VITEST="0"
    fi
}

# Function to get new metrics
get_new_metrics() {
    # Backend coverage
    if [ -f "apps/backend/coverage.xml" ]; then
        NEW_BACKEND=$(grep 'line-rate=' apps/backend/coverage.xml | head -1 | sed 's/.*line-rate="\([^"]*\)".*/\1/' | awk '{printf "%.0f", $1*100}' 2>/dev/null || echo "0")
    else
        NEW_BACKEND="0"
    fi
    
    # Security issues
    if command -v snyk >/dev/null 2>&1; then
        NEW_SNYK=$(snyk test --file=apps/backend/requirements.txt --severity-threshold=high 2>/dev/null | grep -o '[0-9]\+ issues' | head -1 | awk '{print $1}' 2>/dev/null || echo "0")
        if [ -z "$NEW_SNYK" ] || ! [[ "$NEW_SNYK" =~ ^[0-9]+$ ]]; then
            NEW_SNYK="0"
        fi
    else
        NEW_SNYK="0"
    fi
    
    # Vitest tests
    NEW_VITEST=$(find apps/frontend -name "*.test.*" -o -name "*.spec.*" | wc -l | tr -d ' ')
}

# Check for significant changes
check_significant_changes() {
    get_current_readme_metrics
    get_new_metrics
    
    local backend_diff=$(echo "$NEW_BACKEND - $CURRENT_BACKEND" | bc -l 2>/dev/null | sed 's/-//' || echo "0")
    local snyk_diff=$(echo "$NEW_SNYK - $CURRENT_SNYK" | bc -l 2>/dev/null | sed 's/-//' || echo "0")
    local vitest_diff=$(echo "$NEW_VITEST - $CURRENT_VITEST" | bc -l 2>/dev/null | sed 's/-//' || echo "0")
    
    # Check thresholds
    if (( $(echo "$backend_diff >= 5" | bc -l 2>/dev/null) )) || \
       (( $(echo "$snyk_diff >= 1" | bc -l 2>/dev/null) )) || \
       (( $(echo "$vitest_diff >= 2" | bc -l 2>/dev/null) )); then
        return 0  # Significant changes found
    else
        return 1  # No significant changes
    fi
}

# Update README with new badges
update_readme() {
    echo "🔄 Generating updated badges..."
    
    # Generate new badges using the existing script
    ./scripts/update-badges.sh > /dev/null 2>&1
    
    if [ -f ".badges-cache.md" ]; then
        echo "✅ Badges generated successfully"
        echo "💡 To apply to README manually: ./scripts/update-readme-badges.sh"
        return 0
    else
        echo "❌ Failed to generate badges"
        return 1
    fi
}

# Main logic
if [ "$SMART_UPDATE" = true ]; then
    echo "🔍 Checking for significant changes..."
    
    if check_significant_changes; then
        echo "📊 Significant changes detected:"
        echo "   Backend Coverage: ${CURRENT_BACKEND}% -> ${NEW_BACKEND}%"
        echo "   Security Issues: ${CURRENT_SNYK} -> ${NEW_SNYK}"
        echo "   Vitest Tests: ${CURRENT_VITEST} -> ${NEW_VITEST}"
        echo ""
        
        if update_readme; then
            echo "✅ README update process completed"
        fi
    else
        echo "✅ No significant changes detected"
        echo "💡 Thresholds: Backend ±5%, Security/Tests ±1-2"
    fi
    
elif [ "$AUTO_UPDATE" = true ]; then
    echo "🔄 Force updating badges..."
    update_readme
    
else
    echo "📊 Generating badges (no README update)..."
    update_readme
fi

echo ""
echo "✅ Badge process completed!"
echo "💡 Use --smart-update for intelligent README updates"
