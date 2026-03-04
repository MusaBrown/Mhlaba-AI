#!/usr/bin/env python3
"""Debug speech issues"""

import pyttsx3
import traceback

print("="*60)
print("SPEECH DEBUG TEST")
print("="*60)
print()

# Test 1: Basic init
print("[TEST 1] Initializing pyttsx3...")
try:
    engine = pyttsx3.init()
    print("  SUCCESS: Engine created")
except Exception as e:
    print(f"  FAILED: {e}")
    traceback.print_exc()
    exit(1)

# Test 2: Get voices
print("\n[TEST 2] Getting voices...")
try:
    voices = engine.getProperty('voices')
    print(f"  Found {len(voices)} voices:")
    for i, v in enumerate(voices[:3]):
        print(f"    {i}: {v.name}")
except Exception as e:
    print(f"  FAILED: {e}")

# Test 3: Set properties
print("\n[TEST 3] Setting properties...")
try:
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    print("  SUCCESS: Properties set")
except Exception as e:
    print(f"  FAILED: {e}")

# Test 4: First speak
print("\n[TEST 4] First speech test...")
print("  You should HEAR: 'First test'")
input("  Press ENTER to test...")
try:
    engine.say("First test")
    engine.runAndWait()
    print("  SUCCESS: First speech done")
except Exception as e:
    print(f"  FAILED: {e}")
    traceback.print_exc()

# Test 5: Second speak (this is where it usually breaks)
print("\n[TEST 5] Second speech test...")
print("  You should HEAR: 'Second test'")
input("  Press ENTER to test...")
try:
    engine.say("Second test")
    engine.runAndWait()
    print("  SUCCESS: Second speech done")
except Exception as e:
    print(f"  FAILED: {e}")
    traceback.print_exc()

# Test 6: Third speak
print("\n[TEST 6] Third speech test...")
print("  You should HEAR: 'Third test'")
input("  Press ENTER to test...")
try:
    engine.say("Third test")
    engine.runAndWait()
    print("  SUCCESS: Third speech done")
except Exception as e:
    print(f"  FAILED: {e}")
    traceback.print_exc()

print("\n" + "="*60)
print("DEBUG COMPLETE")
print("="*60)
input("\nPress Enter to exit...")
