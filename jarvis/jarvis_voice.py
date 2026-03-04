#!/usr/bin/env python3
"""
JARVIS - Ultra Simple Voice Mode
Works exactly like the diagnostic
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
from ai_brain import AIBrain
import sys

print("="*60)
print("JARVIS VOICE MODE")
print("="*60)

# Setup speech recognition (exactly like diagnostic)
recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

# Setup TTS
print("[INIT] Setting up voice...")
engine = pyttsx3.init()
engine.setProperty('rate', 175)

# Setup AI brain
print("[INIT] Loading AI brain...")
brain = AIBrain()

def speak(text):
    """Speak text"""
    print(f"[JARVIS] {text}")
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
                print("[Could not understand - try speaking louder/clearer]")
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
        speak("Hello! How may I assist you?")
        return True
    
    # Identity
    if 'who are you' in command:
        speak("I am JARVIS, your AI assistant!")
        return True
    
    # Joke
    if 'joke' in command:
        import asyncio
        joke = asyncio.run(brain.generate_response("tell me a joke"))
        speak(joke)
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

speak("JARVIS online. Say a command or 'exit' to quit.")

print("\n" + "="*60)
print("COMMANDS TO TRY:")
print("  - 'Hello'")
print("  - 'What time is it'")
print("  - 'Who are you'")
print("  - 'Tell me a joke'")
print("  - 'Exit'")
print("="*60)

while True:
    text = listen()
    if text:
        if not process(text):
            break

print("\n[JARVIS shutdown]")
