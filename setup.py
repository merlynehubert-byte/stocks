#!/usr/bin/env python3
"""
Setup script for Stock Trading Education Hub
Installs dependencies and checks system requirements
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_streamlit():
    """Check if Streamlit is working"""
    print("\n🔍 Checking Streamlit installation...")
    try:
        result = subprocess.run([sys.executable, "-m", "streamlit", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Streamlit version: {result.stdout.strip()}")
            return True
        else:
            print("❌ Streamlit not working properly")
            return False
    except Exception as e:
        print(f"❌ Error checking Streamlit: {e}")
        return False

def main():
    print("🚀 Stock Trading Education Hub Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check Streamlit
    if not check_streamlit():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run the app:")
    print("1. Run: python run_app.py")
    print("2. Or run directly: streamlit run improved_app.py")
    print("\nThe app will open in your browser at http://localhost:8501")

if __name__ == "__main__":
    main() 