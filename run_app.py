#!/usr/bin/env python3
"""
Stock Trading Education Hub Launcher
Choose which version of the app to run
"""

import subprocess
import sys
import os

def main():
    print("🚀 Stock Trading Education Hub Launcher")
    print("=" * 50)
    print("Choose which version to run:")
    print("1. 🚀 Improved App (Recommended) - Latest features with AI analysis")
    print("2. 📊 Advanced App - Advanced features and real-time data")
    print("3. 📈 Enhanced App - Enhanced UI and examples")
    print("4. 📚 Basic App - Simple educational content")
    print("5. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n🚀 Starting Improved App...")
                subprocess.run([sys.executable, "-m", "streamlit", "run", "improved_app.py"])
                break
            elif choice == "2":
                print("\n📊 Starting Advanced App...")
                subprocess.run([sys.executable, "-m", "streamlit", "run", "advanced_app.py"])
                break
            elif choice == "3":
                print("\n📈 Starting Enhanced App...")
                subprocess.run([sys.executable, "-m", "streamlit", "run", "enhanced_app.py"])
                break
            elif choice == "4":
                print("\n📚 Starting Basic App...")
                subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
                break
            elif choice == "5":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    main() 