#!/usr/bin/env python3
"""
JARVIS - Genius AI Version
Full GPT-4 powered JARVIS with advanced capabilities
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os
import sys
import json

print("="*60)
print("JARVIS - GENIUS AI VERSION")
print("="*60)

# Setup OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("[!] Run: pip install openai")

# Setup speech
recognizer = sr.Recognizer()
microphone = sr.Microphone()
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

# API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_AI = OPENAI_AVAILABLE and OPENAI_API_KEY

if USE_AI:
    client = OpenAI(api_key=OPENAI_API_KEY)
    print("[✓] AI Brain connected (GPT-4)")
else:
    print("[!] Running without AI - set OPENAI_API_KEY for full power")

# Conversation memory (global)
conversation_history = []

def get_history():
    global conversation_history
    return conversation_history

def add_to_history(role, content):
    global conversation_history
    conversation_history.append({"role": role, "content": content})
    # Keep only last 10 exchanges (20 messages)
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

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
        print(f"[Speech error]")

def listen():
    """Listen for command"""
    with microphone as source:
        print("\n[LISTENING...]")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("[Processing speech...]")
            text = recognizer.recognize_google(audio)
            print(f"[You said: '{text}']")
            return text
        except sr.UnknownValueError:
            print("[Didn't catch that - try again]")
            return None
        except:
            return None

def ask_ai(question):
    """Ask GPT-4 with full conversation context"""
    global conversation_history
    
    if not USE_AI:
        return None
    
    try:
        print("[🧠 Thinking...]")
        
        # Build messages with context
        messages = [
            {"role": "system", "content": """You are JARVIS from Iron Man - a brilliant, witty, and helpful AI assistant. 
You have access to the user's computer and can help with tasks, answer questions, explain complex topics, write code, 
analyze problems, and have engaging conversations. Be conversational, use occasional humor, and adapt your response 
length to the question - short for simple queries, detailed for complex ones."""}
        ]
        
        # Add recent conversation context
        if conversation_history:
            for msg in conversation_history[-10:]:
                messages.append(msg)
        
        # Add current question
        messages.append({"role": "user", "content": question})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.8
        )
        
        answer = response.choices[0].message.content
        
        # Store in history
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": answer})
        
        # Keep only last 10 exchanges
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]
        
        return answer
        
    except Exception as e:
        print(f"[AI Error: {e}]")
        import traceback
        traceback.print_exc()
        return "I'm having trouble accessing my advanced neural networks right now."

def process(command):
    """Process command"""
    cmd_lower = command.lower().strip().replace("jarvis", "").strip()
    
    if not cmd_lower:
        return True
    
    # System commands
    if cmd_lower in ['exit', 'quit', 'goodbye', 'bye']:
        speak("Shutting down. It was a pleasure assisting you, sir.")
        return False
    
    if 'time' in cmd_lower:
        speak(f"The time is {datetime.now().strftime('%I:%M %p')}")
        return True
    
    if 'date' in cmd_lower or 'day is it' in cmd_lower:
        speak(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}")
        return True
    
    if cmd_lower.startswith('open '):
        app = cmd_lower.replace('open ', '').strip()
        speak(f"Opening {app}")
        os.system(f'start {app}')
        return True
    
    if 'search' in cmd_lower:
        query = cmd_lower.replace('search', '').replace('for', '').strip()
        speak(f"Searching for {query}")
        import webbrowser
        webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
        return True
    
    if 'weather' in cmd_lower:
        speak("I'll open the weather for you")
        import webbrowser
        webbrowser.open("https://weather.com")
        return True
    
    # Use AI for everything else
    ai_response = ask_ai(command)
    if ai_response:
        speak(ai_response)
    else:
        # Fallback responses
        FALLBACKS = {
            "hello": "Hello sir! JARVIS at your service.",
            "hi": "Greetings! How may I assist?",
            "who are you": "I am JARVIS - Just A Rather Very Intelligent System, your AI assistant.",
            "how are you": "All systems functioning optimally, thank you for asking.",
            "what can you do": "I can answer questions, help with tasks, open applications, search the web, and have intelligent conversations.",
            "tell me a joke": "Why did the programmer quit his job? Because he didn't get arrays!",
            "thank": "You're most welcome, sir.",
        }
        for key, resp in FALLBACKS.items():
            if key in cmd_lower:
                speak(resp)
                return True
        speak("I'm not sure I understood. Could you rephrase that?")
    
    return True

# Main
print("[Calibrating microphone...]")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

print("\n" + "="*60)
if USE_AI:
    print("🔥 GENIUS JARVIS ACTIVATED")
    print("   Powered by GPT-4 - Ask me anything!")
else:
    print("🤖 JARVIS BASIC MODE")
    print("   Set OPENAI_API_KEY for full intelligence")
print("="*60)

if USE_AI:
    speak("JARVIS fully operational with advanced AI capabilities. I am ready to assist you with any task or question.")
else:
    speak("JARVIS online. Basic mode activated.")

print("\n💡 EXAMPLES:")
print('  "Explain quantum computing"')
print('  "Write a Python script to sort files"')
print('  "Help me understand machine learning"')
print('  "What is the theory of relativity?"')
print('  "Open chrome" | "What time is it" | "Exit"')
print("="*60)

while True:
    text = listen()
    if text and not process(text):
        break

print("\n[Shutdown complete]")
