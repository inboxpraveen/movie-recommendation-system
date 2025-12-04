#!/bin/bash
# Setup script for macOS/Linux - Movie Recommendation System

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "\n${BLUE}============================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================================${NC}\n"
}

print_step() {
    echo -e "${GREEN}[$1]${NC} $2"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Main setup
print_header "Movie Recommendation System - Setup"

# Check if Python is installed
print_step "1/7" "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

python3 --version

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_error "Python $REQUIRED_VERSION or higher is required!"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
print_step "2/7" "Setting up virtual environment..."
if [ -d "venv" ]; then
    print_info "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Removing existing virtual environment..."
        rm -rf venv
        python3 -m venv venv
    fi
else
    python3 -m venv venv
fi

# Activate virtual environment
print_step "3/7" "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_step "4/7" "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_step "5/7" "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
print_step "6/7" "Setting up environment file..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_info "Created .env file from template"
    else
        cat > .env << EOF
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
        print_info "Created basic .env file"
    fi
else
    print_info ".env file already exists"
fi

# Create logs directory
if [ ! -d "logs" ]; then
    mkdir -p logs
    print_info "Created logs directory"
fi

# Make build.sh executable
if [ -f "build.sh" ]; then
    chmod +x build.sh
fi

# Run migrations
print_step "7/7" "Running database migrations..."
python manage.py migrate

# Success message
print_header "Setup Complete! 🎉"

echo "Your Movie Recommendation System is ready to use!"
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment:"
echo "     ${GREEN}source venv/bin/activate${NC}"
echo ""
echo "  2. Start the development server:"
echo "     ${GREEN}python manage.py runserver${NC}"
echo ""
echo "  3. Open your browser:"
echo "     ${GREEN}http://localhost:8000${NC}"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Full documentation"
echo "   - QUICKSTART.md - Quick start guide"
echo "   - DEPLOYMENT.md - Deployment guide"
echo ""
echo "💡 Tips:"
echo "   - Edit .env file to customize settings"
echo "   - Run 'python manage.py test' to run tests"
echo ""
echo "🆘 Need help?"
echo "   https://github.com/yourusername/movie-recommendation-system"
echo ""

# Ask if user wants to start server
read -p "Do you want to start the development server now? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    print_info "Starting development server..."
    python manage.py runserver
fi

