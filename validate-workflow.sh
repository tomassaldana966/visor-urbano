#!/bin/bash

echo "🔍 Validating GitHub Actions Workflow for Python..."
echo "=================================================="

# Change to the project root directory
cd "$(dirname "$0")"

# 1. Validate project structure
echo "1. ✅ Validating project structure..."
if [ ! -d "apps/backend" ]; then
    echo "❌ Directory apps/backend not found"
    exit 1
fi

if [ ! -f "apps/backend/requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

if [ ! -d "apps/backend/tests" ]; then
    echo "❌ Directory tests not found"
    exit 1
fi

# 2. Validate workflow YAML
echo "2. ✅ Validating workflow syntax..."
if [ ! -f ".github/workflows/test.yml" ]; then
    echo "❌ Workflow test.yml not found"
    exit 1
fi

python3 -c "
import yaml
try:
    with open('.github/workflows/test.yml', 'r') as f:
        yaml.safe_load(f)
    print('   ✅ Valid YAML syntax')
except Exception as e:
    print(f'   ❌ YAML error: {e}')
    exit(1)
"

# 3. Simulate workflow commands
echo "3. ✅ Simulating workflow commands..."
cd apps/backend

echo "   - Checking Python..."
python3 --version || { echo "❌ Python not found"; exit 1; }

echo "   - Checking pip..."
pip3 --version || { echo "❌ pip not found"; exit 1; }

echo "   - Checking pytest..."
python3 -m pytest --version || { echo "❌ pytest not available"; exit 1; }

# 4. Run tests
echo "4. ✅ Running tests..."
python3 -m pytest tests/ -v --tb=short

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Validation successful!"
    echo "✅ The workflow is correctly configured"
    echo "✅ All tests pass"
    echo "✅ Ready to run on GitHub Actions"
else
    echo ""
    echo "❌ Some tests failed"
    echo "❌ Check the errors before committing"
    exit 1
fi
