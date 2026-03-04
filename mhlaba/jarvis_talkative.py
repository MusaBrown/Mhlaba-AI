#!/usr/bin/env python3
"""
JARVIS - Talkative Version
Recreates speech engine for every response
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os

print("="*60)
print("JARVIS - TALKATIVE VERSION")
print("="*60)

# Setup speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

def speak(text):
    """Create new engine each time to ensure it works"""
    print(f"\n🔊 JARVIS: \"{text}\"")
    try:
        # Create fresh engine each time
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        # Clean up
        engine.stop()
    except Exception as e:
        print(f"[Speech error: {e}]")

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
    command = command.lower().strip().replace("jarvis", "").strip()
    
    if not command:
        return True
    
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
    
    # Greetings
    if any(x in command for x in ['hello', 'hi', 'hey']):
        speak("Hello sir! How may I assist you today?")
        return True
    
    # Identity
    if 'who are you' in command:
        speak("I am JARVIS, Just A Rather Very Intelligent System, your personal AI assistant.")
        return True
    
    # Capabilities
    if 'what can you do' in command:
        speak("I can tell you the time, open applications, have conversations, and assist with various tasks.")
        return True
    
    # Jokes
    if 'joke' in command:
        speak("Why did the scarecrow win an award? Because he was outstanding in his field.")
        return True
    
    # Status
    if 'status' in command or 'how are you' in command:
        speak("All systems are functioning at peak efficiency, thank you for asking.")
        return True
    
    # Thanks
    if any(x in command for x in ['thank you', 'thanks']):
        speak("You're welcome, sir. Always happy to assist.")
        return True
    
    # Open apps
    if command.startswith('open '):
        app = command.replace('open ', '').strip()
        speak(f"Opening {app}")
        try:
            os.system(f'start {app}')
        except:
            pass
        return True
    
    # List files
    if 'list files' in command or 'show files' in command:
        files = os.listdir('.')
        speak(f"Found {len(files)} files in current directory")
        print(f"Files: {files[:10]}")
        return True
    
    # System info
    if 'system info' in command:
        speak("System information displayed on screen")
        return True
    
    # Weather (placeholder)
    if 'weather' in command:
        speak("I don't have access to weather data yet, but I can open a browser for you.")
        return True
    
    # Default
    speak("I understand. I am processing your request.")
    return True

# Main
print("[INIT] Calibrating microphone...")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
print(f"[INIT] Ready!")

print("\n" + "="*60)
print("🔊 TURN UP YOUR VOLUME!")
print("="*60)

# Startup
speak("JARVIS online. Systems operational. How may I assist you today?")

print("\nSay: Hello | What time is it | Who are you")
print("     Tell me a joke | Open notepad | Exit")
print("="*60)

while True:
    text = listen()
    if text:
        if not process(text):
            break

print("\n[JARVIS shutdown]")
