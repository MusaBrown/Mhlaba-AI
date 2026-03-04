#!/usr/bin/env python3
"""
JARVIS - PowerShell Voice Version (Most Reliable)
Uses Windows native speech through PowerShell
"""

import speech_recognition as sr
from datetime import datetime
import os
import random
import subprocess
import time

print("="*60)
print("JARVIS - POWERSHELL VOICE EDITION")
print("="*60)

USER_NAME = "sir"

# Setup speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

def speak(text):
    """Speak using PowerShell (reliable Windows method)"""
    global USER_NAME
    text = text.replace("{name}", USER_NAME)
    
    print(f"\nJARVIS: {text}")
    
    try:
        # Shorten text for speech to avoid long waits
        speech_text = text[:200] if len(text) > 200 else text
        
        # Escape quotes for PowerShell
        safe_text = speech_text.replace('"', '`"').replace("'", "`'")
        
        # PowerShell command for speech - use non-blocking SpeakAsync
        ps_cmd = f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Speak("{safe_text}");'
        
        # Fire and forget - don't wait
        subprocess.Popen(
            ['powershell.exe', '-WindowStyle', 'Hidden', '-Command', ps_cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Short pause to prevent JARVIS hearing itself
        time.sleep(0.3)
        
    except Exception as e:
        print(f"[Voice error: {e}]")

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
    except:
        pass

def ask_ai(question):
    """Ask AI"""
    if not USE_GROQ or not groq_client:
        return None
    try:
        print("[AI thinking...]")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"You are JARVIS from Iron Man. Address user as {USER_NAME}. Be witty and concise. Keep responses short."},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except:
        return None

def process(command):
    """Process command"""
    global USER_NAME
    cmd = command.lower().strip()
    
    if cmd.startswith("jarvis"):
        cmd = cmd[6:].strip()
    
    if not cmd:
        return True
    
    print(f"[Command: {cmd}]")
    
    if cmd in ['exit', 'quit', 'goodbye', 'bye']:
        speak("Goodbye. JARVIS standing by.")
        return False
    
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
    
    if 'time' in cmd:
        t = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {t}, {USER_NAME}.")
        return True
    
    if 'date' in cmd or 'day' in cmd:
        d = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {d}.")
        return True
    
    if cmd.startswith('open '):
        app = cmd[5:].strip()
        speak(f"Opening {app}.")
        os.system(f'start {app}')
        return True
    
    if cmd.startswith('search '):
        query = cmd[7:].strip()
        speak(f"Searching for {query}.")
        import webbrowser
        webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
        return True
    
    if any(x in cmd for x in ['hello', 'hi', 'hey']):
        speak(f"Hello, {USER_NAME}. How may I assist you?")
        return True
    
    if 'how are you' in cmd:
        speak(f"All systems operational, {USER_NAME}.")
        return True
    
    if 'who are you' in cmd:
        speak("I am JARVIS. Just A Rather Very Intelligent System.")
        return True
    
    if 'what can you do' in cmd:
        speak("I can tell you the time, open applications, search the web, and answer questions.")
        return True
    
    if 'joke' in cmd:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "There are 10 types of people: those who understand binary, and those who don't.",
        ]
        speak(random.choice(jokes))
        return True
    
    if 'thank' in cmd:
        speak(f"You're very welcome, {USER_NAME}.")
        return True
    
    ai_response = ask_ai(command)
    if ai_response:
        speak(ai_response)
        return True
    
    speak(f"I didn't catch that, {USER_NAME}. Could you rephrase?")
    return True

# Calibrate mic
print("[Calibrating...]")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

print("\n" + "="*60)
print("JARVIS IS READY")
print("="*60)

speak("Hello. JARVIS online and ready to assist you.")

print("\nCommands: hello | what time | open notepad | my name is Musa | exit")
print("="*60)

while True:
    text = listen()
    if text:
        if not process(text):
            break

print("\n[Shutdown complete]")
