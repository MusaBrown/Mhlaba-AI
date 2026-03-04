#!/usr/bin/env python3
"""
JARVIS - Fixed Voice Version
"""

import speech_recognition as sr
from datetime import datetime
import os
import random
import pyttsx3
import sys

# Force UTF-8 for Windows
sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("JARVIS - FIXED VOICE EDITION")
print("="*60)

USER_NAME = "sir"

# Setup speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

print("[INIT] Initializing voice engine...")

# Initialize engine ONCE at startup
_engine = None
_voice_id = None

def init_engine():
    """Initialize the speech engine"""
    global _engine, _voice_id
    try:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', 170)
        _engine.setProperty('volume', 1.0)
        
        # Find a good voice
        voices = _engine.getProperty('voices')
        for voice in voices:
            if "David" in voice.name or "Zira" in voice.name:
                _voice_id = voice.id
                _engine.setProperty('voice', _voice_id)
                print(f"[INIT] Using voice: {voice.name}")
                break
        
        # Test speak
        _engine.say("Voice ready")
        _engine.runAndWait()
        print("[INIT] Voice test complete")
        return True
    except Exception as e:
        print(f"[INIT ERROR] {e}")
        return False

def speak(text):
    """Speak text reliably"""
    global USER_NAME, _engine
    text = text.replace("{name}", USER_NAME)
    
    print(f"\nJARVIS: {text}")
    
    try:
        # Use the global engine
        if _engine is None:
            print("[ERROR] Speech engine not initialized")
            return
            
        # Shorten for speech
        speech_text = text[:280] if len(text) > 280 else text
        
        print("[SPEAKING...]")
        _engine.say(speech_text)
        _engine.runAndWait()
        print("[DONE SPEAKING]")
        
    except Exception as e:
        print(f"[SPEAK ERROR] {e}")
        import traceback
        traceback.print_exc()

def listen():
    """Listen for command"""
    with microphone as source:
        print("\n[Listening...]")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("[Processing...]")
            text = recognizer.recognize_google(audio)
            print(f"[You: {text}]")
            return text
        except sr.UnknownValueError:
            print("[Did not understand]")
            return None
        except sr.WaitTimeoutError:
            print("[No speech detected]")
            return None
        except Exception as e:
            print(f"[Error: {e}]")
            return None

# Groq setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
USE_GROQ = False
groq_client = None
if GROQ_API_KEY:
    try:
        import groq
        groq_client = groq.Client(api_key=GROQ_API_KEY)
        USE_GROQ = True
        print("[INIT] AI connected")
    except Exception as e:
        print(f"[INIT] AI offline: {e}")
else:
    print("[INIT] AI offline (set GROQ_API_KEY for smart responses)")

def ask_ai(question):
    """Ask AI"""
    if not USE_GROQ or not groq_client:
        return None
    try:
        print("[AI thinking...]")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"You are JARVIS from Iron Man. Address user as {USER_NAME}. Be witty and concise. Keep responses under 2 sentences."},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[AI error: {e}]")
        return None

def process(command):
    """Process command"""
    global USER_NAME
    cmd = command.lower().strip()
    
    # Remove jarvis prefix
    if cmd.startswith("jarvis"):
        cmd = cmd[6:].strip()
    
    if not cmd:
        return True
    
    print(f"[Command: {cmd}]")
    
    # Exit
    if cmd in ['exit', 'quit', 'goodbye', 'bye']:
        speak("Goodbye. JARVIS standing by.")
        return False
    
    # Name
    if "my name is" in cmd:
        name = cmd.split("my name is")[-1].strip().title()
        if name:
            USER_NAME = name
            speak(f"Pleasure to meet you, {USER_NAME}.")
            return True
    
    if "call me" in cmd:
        name = cmd.split("call me")[-1].strip().title()
        if name:
            USER_NAME = name
            speak(f"Very well, {USER_NAME}.")
            return True
    
    if "what is my name" in cmd:
        speak(f"You are {USER_NAME}.")
        return True
    
    # Time
    if 'time' in cmd:
        t = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {t}, {USER_NAME}.")
        return True
    
    # Date
    if 'date' in cmd or 'day' in cmd:
        d = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {d}.")
        return True
    
    # Open
    if cmd.startswith('open '):
        app = cmd[5:].strip()
        speak(f"Opening {app}.")
        os.system(f'start {app}')
        return True
    
    # Search
    if cmd.startswith('search '):
        query = cmd[7:].strip()
        speak(f"Searching for {query}.")
        import webbrowser
        webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
        return True
    
    # Greetings
    if any(x in cmd for x in ['hello', 'hi', 'hey']):
        speak(f"Hello, {USER_NAME}. How may I assist you?")
        return True
    
    # How are you
    if 'how are you' in cmd:
        speak(f"All systems operational, {USER_NAME}.")
        return True
    
    # Who are you
    if 'who are you' in cmd:
        speak("I am JARVIS. Just A Rather Very Intelligent System.")
        return True
    
    # What can you do
    if 'what can you do' in cmd:
        speak("I can tell you the time, open applications, search the web, and answer questions.")
        return True
    
    # Jokes
    if 'joke' in cmd:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "There are 10 types of people: those who understand binary, and those who don't.",
        ]
        speak(random.choice(jokes))
        return True
    
    # Thanks
    if 'thank' in cmd:
        speak(f"You're very welcome, {USER_NAME}.")
        return True
    
    # Weather
    if 'weather' in cmd:
        speak("I don't have direct weather access, but I can open a browser for you.")
        import webbrowser
        webbrowser.open("https://weather.com")
        return True
    
    # Try AI
    ai_response = ask_ai(command)
    if ai_response:
        speak(ai_response)
        return True
    
    # Default
    speak(f"I didn't catch that, {USER_NAME}. Could you rephrase?")
    return True

# Initialize engine
if not init_engine():
    print("[FATAL] Could not initialize voice engine")
    exit(1)

# Calibrate mic
print("[Calibrating microphone...]")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

print("\n" + "="*60)
print("JARVIS IS READY")
print("="*60)

speak("Hello. JARVIS online and ready to assist you.")

print("\nCommands:")
print('  "Hello" | "What time is it" | "My name is Musa"')
print('  "Tell me a joke" | "Open notepad" | "Exit"')
print("="*60)

while True:
    text = listen()
    if text:
        if not process(text):
            break

print("\n[Shutdown complete]")
