#!/usr/bin/env python3
"""
JARVIS Setup Script
Helps install dependencies and configure the assistant
"""

import subprocess
import sys
import os


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    
    # Try regular install first
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("⚠️  Some packages failed to install.")
        print(result.stderr)
        
        # Try installing pyaudio via pipwin on Windows
        if sys.platform == "win32":
            print("\n🔄 Trying alternative PyAudio install...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pipwin"])
            subprocess.run([sys.executable, "-m", "pipwin", "install", "pyaudio"])
    else:
        print("✅ Requirements installed successfully!")
        
    return True


def configure_api_keys():
    """Guide user to configure API keys"""
    print("\n" + "="*50)
    print("🔑 Optional: AI API Keys Configuration")
    print("="*50)
    print("""
JARVIS can work without API keys using its built-in AI.
However, for smarter responses, you can add:

1. OpenAI API Key (for GPT-3.5/GPT-4):
   Set environment variable: OPENAI_API_KEY
   
2. Anthropic API Key (for Claude):
   Set environment variable: ANTHROPIC_API_KEY

To set environment variables on Windows:
   setx OPENAI_API_KEY "your-key-here"
   setx ANTHROPIC_API_KEY "your-key-here"

Then restart your terminal.
""")
    
    check = input("Have you set up API keys? (y/n): ").lower()
    return check in ['y', 'yes']


def test_voice():
    """Test voice synthesis"""
    print("\n🔊 Testing voice synthesis...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say("JARVIS voice test successful. Systems operational.")
        engine.runAndWait()
        print("✅ Voice test passed!")
        return True
    except Exception as e:
        print(f"⚠️  Voice test failed: {e}")
        return False


def main():
    """Main setup process"""
    print("="*50)
    print("🤖 JARVIS Setup")
    print("="*50)
    
    # Check Python
    if not check_python_version():
        sys.exit(1)
        
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed!")
        sys.exit(1)
        
    # Test voice
    test_voice()
    
    # API keys
    configure_api_keys()
    
    print("\n" + "="*50)
    print("✅ Setup Complete!")
    print("="*50)
    print("""
You can now run JARVIS:

  Method 1: Double-click launch_jarvis.bat
  Method 2: Run 'python main.py' in the jarvis folder

Enjoy your AI assistant!
""")


if __name__ == "__main__":
    main()
