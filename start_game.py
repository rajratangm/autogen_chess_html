#!/usr/bin/env python3
"""
Startup script for the Human vs AI Chess Game
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("📝 Please create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        return False
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env file!")
        return False
    
    print("✅ Environment check passed")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = ['flask', 'flask-cors', 'autogen-agentchat', 'autogen-core', 'autogen_ext']
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not found")
            print(f"   Install with: pip install {package}")
            return False
    
    print("✅ All dependencies found")
    return True

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Chess Game Server...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("🎮 Open your browser and start playing!")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for playing!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("♟️  Human vs AI Chess Game")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment setup failed. Please fix the issues above.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing packages.")
        return
    
    print("\n✅ All checks passed!")
    print("🎯 You're playing as White, AI plays as Black")
    print("📋 Game rules:")
    print("   - Make your move by clicking on a piece and then a destination square")
    print("   - The AI will automatically respond with its move")
    print("   - Use 'New Game' to start over, 'Undo' to take back moves")
    print()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
