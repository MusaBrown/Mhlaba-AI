#!/usr/bin/env python3
"""
Voice Diagnostic Tool for JARVIS
Figures out why voice isn't working
"""

import speech_recognition as sr
import time

print("="*60)
print("JARVIS VOICE DIAGNOSTIC")
print("="*60)
print()

# Test 1: List microphones
print("[TEST 1] Available Microphones:")
mics = sr.Microphone.list_microphone_names()
for i, mic in enumerate(mics[:5]):  # Show first 5
    print(f"  {i}: {mic}")
print()

# Test 2: Try to listen with debug output
print("[TEST 2] Recording Test")
print("When you see '>>> RECORDING <<<', say something loudly!")
print()

r = sr.Recognizer()
r.energy_threshold = 3000  # Fixed high threshold
r.dynamic_energy_threshold = False  # Don't auto-adjust
r.pause_threshold = 1.0

with sr.Microphone() as source:
    print(f"Energy threshold set to: {r.energy_threshold}")
    print()
    
    input("Press ENTER to start recording...")
    print()
    print(">>> RECORDING - SPEAK NOW! <<<")
    print("(Say something like 'Hello' loudly)")
    
    try:
        # Record for max 5 seconds
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        
        print()
        print(">>> AUDIO CAPTURED <<<")
        print(f"Audio data length: {len(audio.get_raw_data())} bytes")
        print()
        
        # Try to recognize
        print("Sending to Google Speech Recognition...")
        try:
            text = r.recognize_google(audio)
            print()
            print("="*60)
            print(f">>> SUCCESS! HEARD: '{text}' <<<")
            print("="*60)
        except sr.UnknownValueError:
            print()
            print("[ERROR] Google couldn't understand the audio")
            print("Possible causes:")
            print("  - Speech was too quiet")
            print("  - Too much background noise")
            print("  - Microphone not picking up voice well")
        except sr.RequestError as e:
            print(f"[ERROR] Google API error: {e}")
            print("Check your internet connection")
            
    except sr.WaitTimeoutError:
        print()
        print("[ERROR] Timeout - No speech detected")
        print("Possible causes:")
        print("  - Microphone is muted")
        print("  - Microphone volume too low")
        print("  - Wrong microphone selected")
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

print()
print("="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)
print()
print("If this test worked but JARVIS doesn't:")
print("  - The issue is in JARVIS's listening loop")
print("  - Try running: python main_simple.py")
print()
print("If this test also failed:")
print("  - Check Windows Privacy > Microphone settings")
print("  - Check your microphone volume in Sound settings")
input("\nPress Enter to exit...")
