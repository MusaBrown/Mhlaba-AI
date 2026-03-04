#!/usr/bin/env python3
"""
JARVIS - Clean Version (No Unicode)
Guaranteed to work on Windows
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os
import random

print("="*60)
print("JARVIS - PERSONALITY EDITION")
print("="*60)

# User info
USER_NAME = "sir"

# Setup speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

print("[INIT] Initializing voice...")

# Setup voice
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 0.9)

# Get voices
voices = engine.getProperty('voices')
print(f"[INIT] Found {len(voices)} voices")
for i, v in enumerate(voices):
    print(f"       {i}: {v.name}")

# Use David (male voice)
for voice in voices:
    if "David" in voice.name:
        engine.setProperty('voice', voice.id)
        print(f"[INIT] Using: {voice.name}")
        break

print("[INIT] Ready")

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

def speak(text):
    """Speak text - NO UNICODE"""
    global USER_NAME
    text = text.replace("{name}", USER_NAME)
    
    # Simple print - NO EMOJIS
    print(f"\nJARVIS: {text}")
    
    try:
        # Create fresh engine each time to avoid hangs
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        
        # Shorten long text for speech
        speech_text = text[:250] if len(text) > 250 else text
        
        print(f"[SPEAKING: {speech_text[:50]}...]")
        engine.say(speech_text)
        engine.runAndWait()
        engine.stop()
        
    except Exception as e:
        print(f"[Voice error: {e}]")
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

def ask_ai(question):
    """Ask AI"""
    if not USE_GROQ or not groq_client:
        return None
    try:
        print("[AI thinking...]")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"You are JARVIS from Iron Man. Address user as {USER_NAME}. Be witty and concise."},
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
        speak("Goodbye. It has been a pleasure assisting you.")
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
        speak(f"All systems operational, thank you for asking, {USER_NAME}.")
        return True
    
    # Who are you
    if 'who are you' in cmd:
        speak(f"I am JARVIS. Just A Rather Very Intelligent System. Your personal AI assistant.")
        return True
    
    # What can you do
    if 'what can you do' in cmd:
        speak("I can tell you the time, open applications, search the web, answer questions, and provide witty commentary on demand.")
        return True
    
    # Jokes
    if 'joke' in cmd:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "There are 10 types of people: those who understand binary, and those who don't.",
            "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
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
    speak(f"I didn't quite catch that, {USER_NAME}. Could you rephrase?")
    return True

# Main
print("[Calibrating...]")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

print("\n" + "="*60)
print("JARVIS IS READY")
print("="*60)

speak("Hello. JARVIS online and ready to assist you.")

print("\nCommands:")
print('  "Hello" | "What time is it" | "My name is Master Brown"')
print('  "Tell me a joke" | "Open notepad" | "Exit"')
print("="*60)

while True:
    text = listen()
    if text:
        if not process(text):
            break

print("\n[Shutdown complete]")
