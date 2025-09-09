#!/bin/bash
# 🏷️ Automatic README Badge Updater
# This script automatically updates the badge section in README.md

echo "🔄 Updating badges in README.md automatically..."

# Generate fresh badges
./scripts/update-badges.sh > /dev/null

# Check if .badges-cache.md exists
if [ ! -f ".badges-cache.md" ]; then
    echo "❌ Error: .badges-cache.md not found"
    echo "   Run first: ./scripts/update-badges.sh"
    exit 1
fi

# Create a temporary file with new README content
echo "📝 Creating backup of current README..."
cp README.md README.md.backup

# Extract current badges from cache
BADGES_CONTENT=$(cat .badges-cache.md)

# Create new README with updated badges
echo "🏷️ Updating badges section..."

# Find the line numbers for badge section
FIRST_BADGE_LINE=$(grep -n "^[![]" README.md | head -1 | cut -d: -f1)
LAST_BADGE_LINE=$(grep -n "^[![]" README.md | tail -1 | cut -d: -f1)

if [ -z "$FIRST_BADGE_LINE" ]; then
    echo "❌ Error: No badges found in README.md"
    exit 1
fi

# Create new README
{
    # Print everything before badges
    head -n $((FIRST_BADGE_LINE - 1)) README.md
    
    # Insert new badges
    cat .badges-cache.md
    
    # Print everything after badges
    tail -n +$((LAST_BADGE_LINE + 1)) README.md
} > README.md.tmp

# Replace original README with updated version
mv README.md.tmp README.md

echo "✅ Badges updated in README.md"
echo ""
echo "📊 Current badges:"
echo "=================="
head -11 README.md | grep "^[![]"
echo ""
echo "💾 Backup available at: README.md.backup"
echo "🔄 To revert: mv README.md.backup README.md"
echo ""
echo "✅ Update completed!"
