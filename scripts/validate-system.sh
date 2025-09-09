#!/bin/bash
# 🔬 System Validation Script
# Validates that the complete security & coverage system is working

echo "🔬 Validating Security & Coverage System"
echo "========================================"

VALIDATION_PASSED=true

# 1. Check required scripts exist
echo ""
echo "📁 Checking script files..."

REQUIRED_SCRIPTS=(
    "scripts/local-snyk.sh"
    "scripts/local-coverage.sh"
    "scripts/analyze-all.sh"
    "scripts/update-badges.sh"
    "scripts/smart-update-badges.sh"
    "scripts/pre-commit-analysis.sh"
)

for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [ -f "$script" ] && [ -x "$script" ]; then
        echo "  ✅ $script"
    else
        echo "  ❌ $script (missing or not executable)"
        VALIDATION_PASSED=false
    fi
done

# 2. Check documentation
echo ""
echo "📚 Checking documentation..."

DOC_FILES=(
    "docs/SECURITY_COVERAGE_SETUP.md"
    ".env.example"
)

for doc in "${DOC_FILES[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ✅ $doc"
    else
        echo "  ❌ $doc (missing)"
        VALIDATION_PASSED=false
    fi
done

# 3. Check .gitignore entries
echo ""
echo "🙈 Checking .gitignore..."

GITIGNORE_ENTRIES=(".badges-cache.md" ".badges-temp.md" ".env")

for entry in "${GITIGNORE_ENTRIES[@]}"; do
    if grep -q "^${entry}$" .gitignore 2>/dev/null; then
        echo "  ✅ $entry ignored"
    else
        echo "  ⚠️  $entry not in .gitignore"
    fi
done

# 4. Test smart update functionality
echo ""
echo "🧠 Testing smart update logic..."

if ./scripts/smart-update-badges.sh --smart-update >/dev/null 2>&1; then
    echo "  ✅ Smart update script works"
else
    echo "  ❌ Smart update script failed"
    VALIDATION_PASSED=false
fi

# 5. Test pre-commit script
echo ""
echo "🪝 Testing pre-commit integration..."

if ./scripts/pre-commit-analysis.sh >/dev/null 2>&1; then
    echo "  ✅ Pre-commit script works"
else
    echo "  ❌ Pre-commit script failed"
    VALIDATION_PASSED=false
fi

# 6. Check badge generation
echo ""
echo "🏷️  Testing badge generation..."

if [ -f ".badges-cache.md" ]; then
    BADGE_COUNT=$(grep -c "img.shields.io" .badges-cache.md)
    if [ "$BADGE_COUNT" -gt 5 ]; then
        echo "  ✅ Badge cache generated ($BADGE_COUNT badges)"
    else
        echo "  ⚠️  Badge cache exists but may be incomplete"
    fi
else
    echo "  ⚠️  Badge cache not found (run scripts to generate)"
fi

# 7. Final validation
echo ""
echo "🎯 Validation Summary"
echo "===================="

if [ "$VALIDATION_PASSED" = true ]; then
    echo "✅ All core components validated successfully!"
    echo ""
    echo "🚀 System is ready for use:"
    echo "   • Pre-commit hooks: Active"
    echo "   • Smart badge updates: Working"
    echo "   • Security scanning: Available"
    echo "   • Coverage analysis: Ready"
    echo ""
    echo "💡 Next steps:"
    echo "   1. Set up tokens in .env (optional)"
    echo "   2. Run: ./scripts/analyze-all.sh"
    echo "   3. Make a test commit to trigger pre-commit analysis"
    
    exit 0
else
    echo "❌ Validation failed - some components need attention"
    echo ""
    echo "🔧 Fix the issues above and run validation again"
    
    exit 1
fi
