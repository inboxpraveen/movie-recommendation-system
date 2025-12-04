"""
Setup script for Movie Recommendation System
Provides easy installation and configuration
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(message):
    """Print a formatted header message."""
    print("\n" + "="*60)
    print(f"  {message}")
    print("="*60 + "\n")

def print_step(step, message):
    """Print a formatted step message."""
    print(f"[{step}] {message}")

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"  → {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"  ✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error: {e}")
        print(f"  Output: {e.stdout}")
        print(f"  Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is 3.10 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("  ℹ .env file already exists, skipping...")
        return True
    
    if not env_example.exists():
        print("  ⚠ .env.example not found, creating basic .env file...")
        with open(env_file, 'w') as f:
            f.write("SECRET_KEY=django-insecure-dev-key-change-in-production\n")
            f.write("DEBUG=True\n")
            f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n")
        return True
    
    try:
        shutil.copy(env_example, env_file)
        print("  ✓ Created .env file from .env.example")
        return True
    except Exception as e:
        print(f"  ✗ Error creating .env file: {e}")
        return False

def create_logs_directory():
    """Create logs directory if it doesn't exist."""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        logs_dir.mkdir(parents=True)
        print("  ✓ Created logs directory")
    else:
        print("  ℹ Logs directory already exists")
    return True

def setup():
    """Main setup function."""
    print_header("Movie Recommendation System - Setup")
    
    print("Welcome! This script will set up your development environment.\n")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python version")
    check_python_version()
    
    # Step 2: Create virtual environment
    print_step(2, "Setting up virtual environment")
    venv_exists = Path("venv").exists()
    
    if venv_exists:
        print("  ℹ Virtual environment already exists")
        response = input("  Do you want to recreate it? (y/N): ").strip().lower()
        if response == 'y':
            print("  → Removing existing virtual environment...")
            shutil.rmtree("venv")
            venv_exists = False
    
    if not venv_exists:
        if not run_command(
            f"{sys.executable} -m venv venv",
            "Creating virtual environment"
        ):
            print("\n❌ Setup failed at virtual environment creation")
            sys.exit(1)
    
    # Determine activation command
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Step 3: Install dependencies
    print_step(3, "Installing dependencies")
    if not run_command(
        f"{pip_cmd} install --upgrade pip",
        "Upgrading pip"
    ):
        print("\n⚠ Warning: Failed to upgrade pip, continuing...")
    
    if not run_command(
        f"{pip_cmd} install -r requirements.txt",
        "Installing project dependencies"
    ):
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Step 4: Create .env file
    print_step(4, "Configuring environment variables")
    if not create_env_file():
        print("\n⚠ Warning: Failed to create .env file")
    
    # Step 5: Create logs directory
    print_step(5, "Creating necessary directories")
    create_logs_directory()
    
    # Step 6: Run migrations
    print_step(6, "Setting up database")
    if not run_command(
        f"{python_cmd} manage.py migrate",
        "Running database migrations"
    ):
        print("\n⚠ Warning: Database migration failed")
    
    # Step 7: Collect static files (optional)
    print_step(7, "Collecting static files (optional)")
    response = input("  Collect static files now? (recommended for production) (y/N): ").strip().lower()
    if response == 'y':
        run_command(
            f"{python_cmd} manage.py collectstatic --noinput",
            "Collecting static files"
        )
    
    # Success message
    print_header("Setup Complete! 🎉")
    
    print("Your Movie Recommendation System is ready to use!\n")
    print("Next steps:\n")
    
    if sys.platform == "win32":
        print("  1. Activate virtual environment:")
        print(f"     {activate_cmd}\n")
    else:
        print("  1. Activate virtual environment:")
        print(f"     {activate_cmd}\n")
    
    print("  2. Start the development server:")
    print("     python manage.py runserver\n")
    
    print("  3. Open your browser:")
    print("     http://localhost:8000\n")
    
    print("📚 Documentation:")
    print("   - README.md - Full documentation")
    print("   - QUICKSTART.md - Quick start guide")
    print("   - DEPLOYMENT.md - Deployment guide")
    print("   - CONTRIBUTING.md - Contributing guidelines\n")
    
    print("💡 Tips:")
    print("   - Edit .env file to customize settings")
    print("   - Check logs/ directory for application logs")
    print("   - Run 'python manage.py test' to run tests\n")
    
    print("🆘 Need help? Visit:")
    print("   https://github.com/yourusername/movie-recommendation-system\n")

if __name__ == "__main__":
    try:
        setup()
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

