#!/usr/bin/env python3
"""
JARVIS - Guaranteed Speaking Version
Max volume and clear speech
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
from ai_brain import AIBrain
import sys

print("="*60)
print("JARVIS - SPEAKING VERSION")
print("="*60)

# Setup speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

# Setup TTS with max volume
print("[INIT] Setting up voice (MAX VOLUME)...")
engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)  # MAX VOLUME

# Get available voices and use a clear one
voices = engine.getProperty('voices')
print(f"[INIT] Available voices: {len(voices)}")
for i, v in enumerate(voices[:3]):
    print(f"  {i}: {v.name}")

if voices:
    engine.setProperty('voice', voices[0].id)
    print(f"[INIT] Using voice: {voices[0].name}")

# Setup AI brain
print("[INIT] Loading AI brain...")
brain = AIBrain()

def speak(text):
    """Speak text with visual confirmation"""
    print(f"\n{'='*60}")
    print(f"🔊 JARVIS SPEAKING:")
    print(f"   \"{text}\"")
    print(f"{'='*60}\n")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for command"""
    with microphone as source:
        print("\n[LISTENING... SPEAK NOW!]")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("[PROCESSING...]")
            
            try:
                text = recognizer.recognize_google(audio)
                print(f"[HEARD: '{text}']")
                return text
            except sr.UnknownValueError:
                print("[Could not understand]")
                return None
            except sr.RequestError as e:
                print(f"[Google error: {e}]")
                return None
        except sr.WaitTimeoutError:
            print("[Timeout - no speech detected]")
            return None

def process(command):
    """Process command"""
    command = command.lower().strip()
    
    # Exit
    if command in ['exit', 'quit', 'goodbye', 'bye']:
        speak("Goodbye!")
        return False
    
    # Time
    if 'time' in command:
        t = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {t}")
        return True
    
    # Date
    if 'date' in command or 'day' in command:
        d = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {d}")
        return True
    
    # Greetings
    if any(x in command for x in ['hello', 'hi', 'hey']):
        speak("Hello sir! How may I assist you today?")
        return True
    
    # Identity
    if 'who are you' in command:
        speak("I am JARVIS, Just A Rather Very Intelligent System, at your service!")
        return True
    
    # Joke
    if 'joke' in command:
        import asyncio
        joke = asyncio.run(brain.generate_response("tell me a joke"))
        speak(joke)
        return True
    
    # Open apps
    if command.startswith('open '):
        app = command.replace('open ', '').strip()
        speak(f"Opening {app}")
        import os
        try:
            os.system(f'start {app}')
        except:
            pass
        return True
    
    # Default AI response
    import asyncio
    response = asyncio.run(brain.generate_response(command))
    speak(response)
    return True

# Main loop
print("[INIT] Calibrating microphone...")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
print(f"[INIT] Ready! Threshold: {recognizer.energy_threshold}")

print("\n" + "="*60)
print("🔊 TURN UP YOUR SPEAKER VOLUME NOW!")
print("="*60)

# Test speech first
speak("Hello sir! JARVIS is online and ready. I can hear you and speak back.")

print("\nCOMMANDS TO TRY:")
print("  - 'Hello'")
print("  - 'What time is it'")
print("  - 'Who are you'")
print("  - 'Tell me a joke'")
print("  - 'Open notepad'")
print("  - 'Exit'")
print("="*60)

while True:
    text = listen()
    if text:
        if not process(text):
            break

speak("Shutting down. Have a good day sir!")
print("\n[JARVIS shutdown]")
