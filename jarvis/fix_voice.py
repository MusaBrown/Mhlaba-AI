#!/usr/bin/env python3
"""
Voice Fix Script for JARVIS on Windows
Installs missing Windows dependencies
"""

import subprocess
import sys


def install_package(package):
    """Install a package using pip"""
    print(f"Installing {package}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✓ {package} installed successfully")
        return True
    else:
        print(f"✗ Failed to install {package}")
        print(result.stderr)
        return False


def main():
    print("="*50)
    print("JARVIS Voice Fix for Windows")
    print("="*50)
    print()
    
    packages = [
        "pywin32",        # Required for Windows TTS
        "comtypes",       # Required for pyttsx3 on Windows
        "pypiwin32",      # Alternative Windows package
    ]
    
    for pkg in packages:
        install_package(pkg)
    
    print()
    print("="*50)
    print("Now installing PyAudio (this may take a while)...")
    print("="*50)
    
    # Try different methods to install PyAudio
    methods = [
        ["pipwin", "install", "pyaudio"],
        [sys.executable, "-m", "pip", "install", "pipwin"],
    ]
    
    # First install pipwin
    print("Installing pipwin...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pipwin"])
    
    print("Installing PyAudio via pipwin...")
    subprocess.run([sys.executable, "-m", "pipwin", "install", "pyaudio"])
    
    print()
    print("="*50)
    print("Testing voice...")
    print("="*50)
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say("Voice test successful. JARVIS is ready.")
        engine.runAndWait()
        print("✓ Voice synthesis working!")
    except Exception as e:
        print(f"✗ Voice test failed: {e}")
    
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        print("✓ Speech recognition module loaded")
    except Exception as e:
        print(f"✗ Speech recognition error: {e}")
    
    print()
    print("="*50)
    print("Fix complete! Try running: python main.py")
    print("="*50)


if __name__ == "__main__":
    main()
