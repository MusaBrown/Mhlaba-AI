#!/usr/bin/env python3
"""
JARVIS - Smart AI Version
Uses OpenAI GPT for intelligent conversations
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os
import sys

print("="*60)
print("JARVIS - SMART AI VERSION")
print("="*60)

# Try to import OpenAI
try:
    import openai
    OPENAI_AVAILABLE = True
    print("[INIT] OpenAI module found")
except ImportError:
    OPENAI_AVAILABLE = False
    print("[INIT] OpenAI not installed. Run: pip install openai")

# Setup speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

# Check for API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_AI = OPENAI_AVAILABLE and OPENAI_API_KEY

if USE_AI:
    openai.api_key = OPENAI_API_KEY
    print("[INIT] OpenAI API configured")
else:
    print("[INIT] Using built-in responses (set OPENAI_API_KEY for smarter AI)")

def speak(text):
    """Speak text"""
    print(f"\n🔊 JARVIS: \"{text}\"")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
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

def ask_openai(question):
    """Ask OpenAI for a response"""
    if not USE_AI:
        return None
    
    try:
        print("[Thinking with AI...]")
        # Try new API format first
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are JARVIS, an AI assistant inspired by Iron Man. Be helpful, witty, and conversational. Keep responses concise (1-2 sentences for simple questions, longer for complex ones)."},
                    {"role": "user", "content": question}
                ],
                max_tokens=250,
                temperature=0.7
            )
            return response.choices[0].message.content
        except:
            # Fallback to old API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are JARVIS, an AI assistant inspired by Iron Man. Be helpful, witty, and conversational."},
                    {"role": "user", "content": question}
                ],
                max_tokens=250,
                temperature=0.7
            )
            return response.choices[0].message.content
    except Exception as e:
        print(f"[AI Error: {e}]")
        return None

def process(command):
    """Process command with AI fallback"""
    command_lower = command.lower().strip().replace("jarvis", "").strip()
    
    if not command_lower:
        return True
    
    # Exit
    if command_lower in ['exit', 'quit', 'goodbye', 'bye']:
        speak("Goodbye sir! JARVIS standing by.")
        return False
    
    # Time
    if 'time' in command_lower:
        t = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {t}")
        return True
    
    # Date
    if 'date' in command_lower or 'day' in command_lower:
        d = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {d}")
        return True
    
    # Open apps
    if command_lower.startswith('open '):
        app = command_lower.replace('open ', '').strip()
        speak(f"Opening {app}")
        try:
            os.system(f'start {app}')
        except:
            pass
        return True
    
    # List files
    if 'list files' in command_lower or 'show files' in command_lower:
        files = os.listdir('.')
        speak(f"Found {len(files)} files")
        print(f"Files: {files[:10]}")
        return True
    
    # Search web
    if 'search' in command_lower or 'look up' in command_lower:
        query = command_lower.replace('search', '').replace('look up', '').strip()
        speak(f"Searching for {query}")
        import webbrowser
        webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
        return True
    
    # Quick built-in responses for common greetings
    QUICK_RESPONSES = {
        "hello": "Hello sir! How may I assist you today?",
        "hi": "Hello! JARVIS at your service.",
        "hey": "Greetings sir!",
        "how are you": "All systems are functioning at peak efficiency, thank you for asking.",
        "who are you": "I am JARVIS, Just A Rather Very Intelligent System, your personal AI assistant inspired by Iron Man.",
        "what can you do": "I can answer questions, tell you the time, open applications, search the web, and have intelligent conversations with you.",
        "what is your name": "My name is JARVIS - Just A Rather Very Intelligent System.",
        "tell me a joke": "Why don't scientists trust atoms? Because they make up everything.",
        "another joke": "Why did the scarecrow win an award? He was outstanding in his field.",
        "thank you": "You're welcome, sir. Always happy to assist.",
        "thanks": "My pleasure, sir.",
        "status": "All systems nominal. Ready for your commands.",
    }
    
    # Check quick responses first
    for key, response in QUICK_RESPONSES.items():
        if key in command_lower:
            speak(response)
            return True
    
    # Use AI for everything else
    if USE_AI:
        ai_response = ask_openai(command)
        if ai_response:
            speak(ai_response)
            return True
    
    # Fallback response
    speak("I'm still learning about that. Try asking me about the time, opening an app, or say 'what can you do' for help.")
    return True

# Main
print("[INIT] Calibrating microphone...")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
print(f"[INIT] Ready!")

print("\n" + "="*60)
if USE_AI:
    print("🔊 SMART JARVIS IS READY (AI Powered)")
else:
    print("🔊 JARVIS IS READY (Basic Mode)")
    print("   For smarter AI, get an OpenAI API key from:")
    print("   https://platform.openai.com/api-keys")
    print("   Then run: setx OPENAI_API_KEY your-key")
print("="*60)

# Startup
if USE_AI:
    speak("JARVIS online with advanced AI capabilities. How may I assist you today?")
else:
    speak("JARVIS online. Systems operational. How may I assist you today?")

print("\nTRY SAYING:")
print("  General: 'Hello' | 'Who are you' | 'What can you do'")
print("  Info: 'What time is it' | 'Search for weather'")
print("  Action: 'Open notepad' | 'List files'")
if USE_AI:
    print("  AI Questions: 'Explain quantum physics' | 'Write a poem'")
print("  Exit: 'Goodbye'")
print("="*60)

# Main loop
conversation_history = []

while True:
    text = listen()
    if text:
        # Add to history
        conversation_history.append(text)
        if len(conversation_history) > 10:
            conversation_history.pop(0)
        
        if not process(text):
            break

print("\n[JARVIS shutdown]")
