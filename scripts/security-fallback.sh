#!/bin/bash
# 🔒 Fallback Security Analysis Script
# This script uses alternative security tools when Snyk is not available

echo "🔒 Fallback Security Analysis"
echo "============================="

echo ""
echo "🌐 FRONTEND (React Router + TypeScript)"
echo "---------------------------------------"
cd apps/frontend
echo "Running npm audit..."
if pnpm audit --audit-level high; then
    echo "✅ No high-level vulnerabilities found in frontend"
else
    echo "⚠️  High-level vulnerabilities found in frontend - review above"
fi

echo ""
echo "🐍 BACKEND (Python + FastAPI)"
echo "-----------------------------"
cd ../backend
echo "Running safety scan..."
if command -v safety >/dev/null 2>&1; then
    if python -m safety scan --short-report; then
        echo "✅ No critical vulnerabilities found in backend"
    else
        echo "⚠️  Vulnerabilities found - review above"
        echo "   Known issues: 2 HIGH vulnerabilities in ecdsa@0.19.1 (documented)"
    fi
else
    echo "⚠️  Safety not available, install with: pip install safety"
    echo "   Known issues: 2 HIGH vulnerabilities in ecdsa@0.19.1 (documented)"
fi

echo ""
echo "📋 ROOT DEPENDENCIES"
echo "--------------------"
cd ../..
echo "Running npm audit on root..."
if pnpm audit --audit-level high; then
    echo "✅ No high-level vulnerabilities found in root dependencies"
else
    echo "⚠️  High-level vulnerabilities found in root - review above"
fi

echo ""
echo "📊 SECURITY SUMMARY"
echo "-------------------"
echo "✅ Frontend: Using npm audit for dependency scanning"
echo "✅ Backend: Using safety for Python dependency scanning"
echo "⚠️  Known issues:"
echo "   • ecdsa@0.19.1: 2 HIGH vulnerabilities (documented, monitoring for fix)"
echo "   • Migration from python-jose to authlib completed"

echo ""
echo "🔧 SECURITY ACTIONS TAKEN"
echo "-------------------------"
echo "✅ Upgraded python-jose to authlib (eliminated JWT vulnerabilities)"
echo "✅ Updated pyasn1 to latest version"
echo "⚠️  ecdsa vulnerabilities remain (no fix available, documented)"

echo ""
echo "🚀 USEFUL COMMANDS"
echo "------------------"
echo "# Check for updates:"
echo "cd apps/frontend && pnpm update"
echo "cd apps/backend && pip list --outdated"
echo ""
echo "# Install security tools:"
echo "pip install safety"
echo "npm install -g audit-ci"

echo ""
echo "✅ Fallback security analysis completed!"
