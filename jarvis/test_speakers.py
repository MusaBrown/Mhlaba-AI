#!/usr/bin/env python3
"""
Speaker Test - Make sure you can hear JARVIS
"""

import pyttsx3

print("="*60)
print("SPEAKER TEST")
print("="*60)
print()
print("🔊 TURN UP YOUR SPEAKER VOLUME!")
print()
input("Press ENTER to test speech...")

print("\n[Testing speech engine...]")
engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)  # Max volume

# Show available voices
voices = engine.getProperty('voices')
print(f"\nFound {len(voices)} voices:")
for i, v in enumerate(voices[:5]):
    print(f"  {i}: {v.name}")

# Test each voice
print("\n" + "="*60)
print("Testing voices (you should hear each one)...")
print("="*60)

for i, voice in enumerate(voices[:3]):
    print(f"\nPlaying voice {i}: {voice.name}")
    engine.setProperty('voice', voice.id)
    engine.say(f"Hello, this is voice number {i}")
    engine.runAndWait()

print("\n" + "="*60)
print("Test complete!")
print("If you heard the voices, JARVIS will work correctly.")
print("If not, check your speakers/headphones and Windows volume.")
print("="*60)

input("\nPress Enter to exit...")
