#!/usr/bin/env python3
"""
JARVIS - Final Working Version
Fixed speech issues
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
import asyncio
import sys

print("="*60)
print("JARVIS - FINAL VERSION")
print("="*60)

# Setup speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

# Setup TTS - create once and reuse
print("[INIT] Setting up voice...")
engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)

# Simple responses (no async needed)
RESPONSES = {
    "hello": "Hello sir! How may I assist you today?",
    "hi": "Hello! JARVIS at your service.",
    "hey": "Greetings sir!",
    "how are you": "All systems are functioning at peak efficiency, thank you for asking.",
    "who are you": "I am JARVIS, Just A Rather Very Intelligent System, your personal AI assistant.",
    "what can you do": "I can tell you the time, open applications, have conversations, and assist with various tasks.",
    "what time is it": None,  # Special handling
    "what day is it": None,   # Special handling
    "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "joke": "Why don't scientists trust atoms? Because they make up everything.",
    "status": "All systems nominal. CPU and memory within normal parameters.",
    "thank you": "You're welcome, sir. Always happy to assist.",
    "thanks": "My pleasure, sir.",
}

def speak(text):
    """Speak text with visual confirmation"""
    print(f"\n🔊 JARVIS: \"{text}\"")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[SPEECH ERROR: {e}]")

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
                print("[Could not understand - try again]")
                return None
            except sr.RequestError as e:
                print(f"[Google error: {e}]")
                return None
        except sr.WaitTimeoutError:
            print("[Timeout - no speech detected]")
            return None

def process(command):
    """Process command - synchronous version"""
    command = command.lower().strip()
    
    # Remove wake word
    command = command.replace("jarvis", "").strip()
    
    # Exit
    if command in ['exit', 'quit', 'goodbye', 'bye']:
        speak("Goodbye sir! JARVIS standing by.")
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
    
    # List files
    if 'list files' in command or 'show files' in command:
        import os
        files = os.listdir('.')
        speak(f"Found {len(files)} files in current directory")
        print(f"Files: {files[:10]}")
        return True
    
    # System info
    if 'system info' in command:
        import psutil
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        speak(f"CPU usage is {cpu} percent. Memory usage is {mem} percent.")
        return True
    
    # Check predefined responses
    for key, response in RESPONSES.items():
        if key in command:
            if response:
                speak(response)
            return True
    
    # Default response
    speak("I understand. I'm processing that request.")
    return True

# Main loop
print("[INIT] Calibrating microphone...")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
print(f"[INIT] Ready! Threshold: {recognizer.energy_threshold}")

print("\n" + "="*60)
print("🔊 JARVIS IS READY - SPEAK NOW")
print("="*60)

# Startup message
speak("JARVIS online. Systems operational. How may I assist you today?")

print("\nCOMMANDS:")
print("  Hello | What time is it | Who are you")
print("  Tell me a joke | Open notepad | System info")
print("  List files | Exit")
print("="*60)

# Conversation loop
while True:
    text = listen()
    if text:
        if not process(text):
            break

print("\n[JARVIS shutdown]")
