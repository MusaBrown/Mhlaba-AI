#!/usr/bin/env python3
"""Quick test for JARVIS voice"""

import pyttsx3
import speech_recognition as sr

print("="*60)
print("JARVIS QUICK VOICE TEST")
print("="*60)
print()

# Test 1: Text-to-Speech
print("[TEST 1] Testing speakers...")
print("You should HEAR: 'Testing speakers'")
print()
input("Press ENTER to test (turn up volume)...")

try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 0.9)
    engine.say("Testing speakers. Can you hear me?")
    engine.runAndWait()
    print("[OK] Speech test complete")
except Exception as e:
    print(f"[ERROR] Speech failed: {e}")

print()
print("="*60)

# Test 2: Microphone
print("[TEST 2] Testing microphone...")
print("Available microphones:")
mics = sr.Microphone.list_microphone_names()
for i, mic in enumerate(mics[:3]):
    print(f"  {i}: {mic}")

print()
input("Press ENTER to test microphone (say something loudly)...")

r = sr.Recognizer()
r.energy_threshold = 3000
r.dynamic_energy_threshold = False

with sr.Microphone() as source:
    print()
    print(">>> SPEAK NOW <<<")
    try:
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        print("[OK] Audio captured!")
        
        print("Processing speech...")
        try:
            text = r.recognize_google(audio)
            print()
            print(">>> SUCCESS! I HEARD:")
            print(f">>> '{text}' <<<")
        except sr.UnknownValueError:
            print("[ERROR] Could not understand audio")
            print("  - Speak louder or closer to mic")
            print("  - Check mic is not muted")
        except sr.RequestError as e:
            print(f"[ERROR] Internet/Google issue: {e}")
            
    except sr.WaitTimeoutError:
        print("[ERROR] No speech detected")
        print("  - Microphone may be muted")
        print("  - Check Windows Privacy > Microphone settings")

print()
print("="*60)
print("TEST COMPLETE")
print("="*60)
input("Press Enter to exit...")
