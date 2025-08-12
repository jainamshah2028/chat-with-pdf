#!/usr/bin/env python3
"""
Deployment and setup script for Enhanced PDF Chat App
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def setup_environment():
    """Setup the environment for the app"""
    print("🚀 Setting up Enhanced PDF Chat App Environment\n")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not os.path.exists(".venv"):
        if not run_command("python -m venv .venv", "Creating virtual environment"):
            return False
    
    # Activate virtual environment (Windows)
    activate_cmd = ".venv\\Scripts\\activate" if os.name == 'nt' else "source .venv/bin/activate"
    pip_cmd = ".venv\\Scripts\\pip" if os.name == 'nt' else ".venv/bin/pip"
    python_cmd = ".venv\\Scripts\\python" if os.name == 'nt' else ".venv/bin/python"
    
    # Upgrade pip
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    if os.path.exists("requirements_enhanced.txt"):
        if not run_command(f"{pip_cmd} install -r requirements_enhanced.txt", "Installing enhanced requirements"):
            return False
    elif os.path.exists("requirements.txt"):
        if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing basic requirements"):
            return False
    else:
        print("❌ No requirements file found")
        return False
    
    # Create necessary directories
    Path("data").mkdir(exist_ok=True)
    Path("data/processed_docs").mkdir(exist_ok=True)
    print("✅ Created data directories")
    
    return True

def run_app(app_file="app_enhanced.py"):
    """Run the Streamlit app"""
    if not os.path.exists(app_file):
        app_file = "app.py"
    
    if not os.path.exists(app_file):
        print(f"❌ App file {app_file} not found")
        return False
    
    streamlit_cmd = ".venv\\Scripts\\streamlit" if os.name == 'nt' else ".venv/bin/streamlit"
    
    print(f"🚀 Starting app: {app_file}")
    print("🌐 App will open in your browser automatically")
    print("📱 Access from other devices using the Network URL")
    print("⏹️  Press Ctrl+C to stop the app\n")
    
    try:
        subprocess.run(f"{streamlit_cmd} run {app_file}", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start app: {e}")
        return False
    
    return True

def main():
    """Main setup and run function"""
    print("=" * 50)
    print("📚 Enhanced PDF Chat App - Setup & Run")
    print("=" * 50)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Setup failed. Please check the errors above.")
        return
    
    print("\n✅ Environment setup complete!")
    print("\nChoose an option:")
    print("1. Run Enhanced App (app_enhanced.py)")
    print("2. Run Basic App (app.py)")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            run_app("app_enhanced.py")
            break
        elif choice == "2":
            run_app("app.py")
            break
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
