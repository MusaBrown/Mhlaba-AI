#!/usr/bin/env python3
"""
Test if Text-to-Speech is working
"""

import pyttsx3

print("="*60)
print("TTS DIAGNOSTIC TEST")
print("="*60)

print("\n1. Checking pyttsx3...")
try:
    engine = pyttsx3.init()
    print("   [OK] pyttsx3 initialized")
except Exception as e:
    print(f"   [FAIL] Error: {e}")
    exit(1)

print("\n2. Getting voices...")
try:
    voices = engine.getProperty('voices')
    print(f"   [OK] Found {len(voices)} voices")
    for i, v in enumerate(voices[:5]):
        print(f"      {i}: {v.name}")
except Exception as e:
    print(f"   [FAIL] Error: {e}")

print("\n3. Setting properties...")
try:
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 0.9)
    print("   [OK] Properties set")
except Exception as e:
    print(f"   [FAIL] Error: {e}")

print("\n4. Attempting to speak...")
print("   You should hear: 'Testing JARVIS voice'")
print("   Listening now...")

try:
    engine.say("Testing JARVIS voice. If you hear this, speech is working.")
    engine.runAndWait()
    print("   [OK] Speech completed!")
except Exception as e:
    print(f"   [FAIL] Speech error: {e}")
    import traceback
    traceback.print_exc()

print("\n5. Testing second speech...")
try:
    engine2 = pyttsx3.init()
    engine2.setProperty('rate', 160)
    engine2.say("Second test. Can you hear me?")
    engine2.runAndWait()
    print("   [OK] Second speech completed!")
except Exception as e:
    print(f"   [FAIL] Second speech error: {e}")

print("\n" + "="*60)
print("Test complete!")
print("="*60)

input("\nPress Enter to exit...")
