#!/bin/bash

# Setup script for Visor Urbano - Complete development environment setup

echo "🚀 Setting up Visor Urbano development environment..."
echo ""

# Function to check if Docker is running
check_docker() {
    echo "🐳 Checking Docker status..."
    if ! command -v docker &> /dev/null; then
        echo ""
        echo "❌ Docker is not installed on your system."
        echo "📥 Please download and install Docker Desktop from:"
        echo "   👉 https://www.docker.com/products/docker-desktop/"
        echo ""
        echo "After installation, please restart this script."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        echo ""
        echo "❌ Docker is installed but not running."
        echo "🔄 Please start Docker Desktop and wait for it to fully load."
        echo "📥 If Docker is not installed, download it from:"
        echo "   👉 https://www.docker.com/products/docker-desktop/"
        echo ""
        echo "After Docker is running, please restart this script."
        exit 1
    fi

    echo "✅ Docker is running and ready!"
    echo ""
}

# Function to copy environment files
setup_env_files() {
    echo "Setting up environment configuration files..."
    echo ""

    # Root .env file
    if [ -f ".env.example" ] && [ ! -f ".env" ]; then
        cp .env.example .env
        echo "✅ Root .env file created from .env.example"
    elif [ -f ".env" ]; then
        echo "ℹ️  Root .env file already exists (skipping)"
    else
        echo "⚠️  Warning: Root .env.example file not found"
    fi

    # Backend .env file
    if [ -f "apps/backend/.env.example" ] && [ ! -f "apps/backend/.env" ]; then
        cp apps/backend/.env.example apps/backend/.env
        echo "✅ Backend .env file created from .env.example"
    elif [ -f "apps/backend/.env" ]; then
        echo "ℹ️  Backend .env file already exists (skipping)"
    else
        echo "⚠️  Warning: Backend .env.example file not found"
    fi

    # Frontend .env file
    if [ -f "apps/frontend/.env.example" ] && [ ! -f "apps/frontend/.env" ]; then
        cp apps/frontend/.env.example apps/frontend/.env
        echo "✅ Frontend .env file created from .env.example"
    elif [ -f "apps/frontend/.env" ]; then
        echo "ℹ️  Frontend .env file already exists (skipping)"
    else
        echo "⚠️  Warning: Frontend .env.example file not found"
    fi

    echo ""
    echo "📝 Note: Please review and update the .env files with your specific configuration:"
    echo "   • Database credentials in apps/backend/.env"
    echo "   • API keys and tokens in apps/backend/.env"
    echo "   • Map configuration in apps/frontend/.env"
    echo ""
}

# Start setup process
check_docker
setup_env_files

# Check Node.js and package manager requirements
echo "📦 Checking Node.js and package manager requirements..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo ""
    echo "❌ Node.js is not installed on your system."
    echo "📥 Please install Node.js from one of these options:"
    echo ""
    echo "   Option 1 - Direct installation:"
    echo "   👉 https://nodejs.org/en"
    echo ""
    echo "   Option 2 - Using nvm (recommended for version management):"
    echo "   👉 Install nvm first: https://github.com/nvm-sh/nvm#installing-and-updating"
    echo "   👉 Then run: nvm install --lts && nvm use --lts"
    echo ""
    echo "After installing Node.js, please restart this script."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2)
MAJOR_VERSION=$(echo $NODE_VERSION | cut -d'.' -f1)

if [ "$MAJOR_VERSION" -lt 18 ]; then
    echo ""
    echo "⚠️  Warning: Node.js version $NODE_VERSION detected. This project requires Node.js 18 or higher."
    echo ""
    echo "📥 Please update Node.js using one of these options:"
    echo ""
    echo "   Option 1 - Direct download:"
    echo "   👉 https://nodejs.org/en (download latest LTS version)"
    echo ""
    echo "   Option 2 - Using nvm (recommended):"
    if ! command -v nvm &> /dev/null; then
        echo "   👉 First install nvm: https://github.com/nvm-sh/nvm#installing-and-updating"
        echo "   👉 Then run: nvm install --lts && nvm use --lts"
    else
        echo "   👉 Run: nvm install --lts && nvm use --lts"
    fi
    echo ""
    echo "After updating Node.js, please restart this script."
    exit 1
fi

echo "✅ Node.js version $NODE_VERSION detected (compatible)"

# Install dependencies
echo "📦 Installing project dependencies..."
if command -v pnpm &> /dev/null; then
    pnpm install
    echo "✅ Dependencies installed successfully with pnpm"
else
    echo ""
    echo "⚠️  pnpm not found. pnpm is the recommended package manager for this project."
    echo ""
    echo "📥 Please install pnpm using one of these methods:"
    echo ""
    echo "   Option 1 - Using npm (if you have npm):"
    echo "   👉 npm install -g pnpm"
    echo ""
    echo "   Option 2 - Using curl (recommended):"
    echo "   👉 curl -fsSL https://get.pnpm.io/install.sh | sh -"
    echo ""
    echo "   Option 3 - Using Homebrew (macOS):"
    echo "   👉 brew install pnpm"
    echo ""
    echo "   For more installation options, visit:"
    echo "   👉 https://pnpm.io/installation"
    echo ""
    echo "Falling back to npm for now..."
    
    if command -v npm &> /dev/null; then
        npm install
        echo "✅ Dependencies installed successfully with npm"
        echo ""
        echo "💡 Tip: Consider installing pnpm for better performance and disk usage:"
        echo "   👉 npm install -g pnpm"
    else
        echo ""
        echo "❌ Neither pnpm nor npm are available."
        echo "📥 Please install Node.js first from: https://nodejs.org/en"
        echo "After installing Node.js, please restart this script."
        exit 1
    fi
fi
echo ""

# Setup Git hooks
echo "🪝 Setting up Git hooks..."
if [ -d ".git" ]; then
    # Create hooks directory if it doesn't exist
    mkdir -p .git/hooks
    
    # Create pre-commit hook
    if [ -f ".husky/pre-commit" ]; then
        ln -sf ../../.husky/pre-commit .git/hooks/pre-commit
        chmod +x .git/hooks/pre-commit
        echo "✅ Pre-commit hook installed successfully"
    else
        echo "❌ .husky/pre-commit not found"
    fi
else
    echo "❌ Not a Git repository - Git hooks setup skipped"
fi

echo ""
echo "🎉 Setup complete! Your Visor Urbano development environment is ready!"
echo ""
echo "Quick Start Commands:"
echo "  pnpm dev              - Start the full development environment"
echo "  pnpm dev:frontend     - Start only the frontend development server"
echo "  pnpm dev:backend      - Start only the backend development server"
echo ""
echo "🔧 Additional Commands:"
echo "  pnpm format           - Format all code with Prettier"
echo "  pnpm test             - Run all tests"
echo "  pnpm typecheck        - Check TypeScript types"
echo "  pnpm build            - Build the entire project"
echo ""
echo "📋 Git Hooks Configured:"
echo "  pre-commit: Automatically runs formatting + type checking on staged files"
echo ""
echo "🔍 Next Steps:"
echo "  1. Review and update .env files with your configuration"
echo "  2. Ensure your database is running (if using local setup)"
echo "  3. Run 'pnpm dev' to start the development environment"
echo ""
echo "🚀 Performance Tip:"
if ! command -v pnpm &> /dev/null; then
    echo "  Consider installing pnpm for better performance:"
    echo "  👉 npm install -g pnpm"
    echo "  👉 Or visit: https://pnpm.io/installation"
    echo ""
fi
echo "🔐 IMPORTANT SECURITY REMINDER:"
echo "  📝 Please review the newly created .env files and update them with your specific configuration:"
echo "     • Root .env file: Update tokens for Snyk and Codecov (if available)"
echo "     • Backend .env file: Change default database passwords and API keys"
echo "     • Frontend .env file: Update map service configurations and API endpoints"
echo ""
echo "  ⚠️  DO NOT use default passwords in production environments!"
echo "  🔒 Make sure to use strong, unique passwords for all database connections"
echo ""
