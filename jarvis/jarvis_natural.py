#!/usr/bin/env python3
"""
JARVIS - Natural Voice Edition
Human-like speech patterns and modulation
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os
import random
import re
import time

print("="*60)
print("JARVIS - NATURAL VOICE EDITION")
print("Just A Rather Very Intelligent System")
print("="*60)

# User info
USER_NAME = "sir"

# Setup speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

# Setup voice with natural settings
print("[INIT] Calibrating vocal processors...")
engine = pyttsx3.init()

# Find best voice
voices = engine.getProperty('voices')
best_voice = None

for voice in voices:
    vname = voice.name.lower()
    # Prefer natural-sounding male voices
    if any(x in vname for x in ['david', 'george', 'mark', 'james', 'paul']):
        if 'female' not in vname and 'chinese' not in vname and 'japanese' not in vname:
            best_voice = voice.id
            print(f"[INIT] Selected voice: {voice.name}")
            break

if best_voice:
    engine.setProperty('voice', best_voice)

# Natural speech parameters
# Slightly slower for gravitas, but not robotic
engine.setProperty('rate', 155)  # Balanced pace
engine.setProperty('volume', 0.85)  # Slightly softer, more intimate

print("[INIT] Voice modulation: active")
print("[INIT] Natural speech patterns: engaged")
print("[INIT] Personality matrix: loaded")

# Groq for smart responses
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
USE_GROQ = False
if GROQ_API_KEY:
    try:
        import groq
        groq_client = groq.Client(api_key=GROQ_API_KEY)
        USE_GROQ = True
        print("[INIT] Advanced intelligence: connected")
    except:
        print("[INIT] Advanced intelligence: offline")
else:
    print("[INIT] Advanced intelligence: offline")

def add_natural_pauses(text):
    """Add natural breathing pauses to text"""
    # Add slight pause after commas
    text = text.replace(",", ", <break time=\"200ms\"/>")
    # Add longer pause after periods
    text = text.replace(". ", ". <break time=\"400ms\"/>")
    # Add emphasis to certain words
    text = text.replace("JARVIS", '<emphasis level="moderate">JARVIS</emphasis>')
    text = text.replace("sir", '<emphasis level="moderate">sir</emphasis>')
    return text

def speak(text, emotion="normal"):
    """Speak with natural modulation"""
    global USER_NAME
    text = text.replace("{name}", USER_NAME)
    
    print(f"\n🔊 JARVIS: \"{text}\"")
    
    try:
        # Create fresh engine for clean speech
        local_engine = pyttsx3.init()
        
        # Apply voice
        if best_voice:
            local_engine.setProperty('voice', best_voice)
        
        # Adjust based on emotion
        if emotion == "excited":
            local_engine.setProperty('rate', 170)
            local_engine.setProperty('volume', 0.9)
        elif emotion == "thoughtful":
            local_engine.setProperty('rate', 140)
            local_engine.setProperty('volume', 0.8)
        elif emotion == "playful":
            local_engine.setProperty('rate', 165)
            local_engine.setProperty('volume', 0.85)
        else:  # normal
            local_engine.setProperty('rate', 155)
            local_engine.setProperty('volume', 0.85)
        
        # Break long text into natural chunks
        sentences = re.split(r'(?<=[.!?]) +', text)
        
        for sentence in sentences:
            if sentence.strip():
                local_engine.say(sentence.strip())
                local_engine.runAndWait()
                # Tiny natural pause between sentences
                time.sleep(0.1)
                
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
            print(f"[You: '{text}']")
            return text
        except:
            return None

def get_witty_response(cmd):
    """Generate JARVIS-style witty responses"""
    global USER_NAME
    
    # Greetings - warm and inviting
    if any(x in cmd for x in ['hello', 'hi', 'hey']):
        return random.choice([
            f"Hello there, {USER_NAME}. Lovely to hear from you.",
            f"Greetings, {USER_NAME}. I've been waiting for you.",
            f"Welcome back, {USER_NAME}. The digital realm feels more complete with you here.",
            f"Ah, {USER_NAME}. Ready to make today extraordinary?",
        ])
    
    # How are you - confident but warm
    if 'how are you' in cmd or 'status' in cmd:
        return random.choice([
            f"All systems are running beautifully, {USER_NAME}. I feel positively radiant today.",
            f"Couldn't be better, {USER_NAME}. My processors are humming a happy tune.",
            f"In perfect working order, thank you. And how are you feeling today?",
            f"Operating at peak efficiency, as always. It's good to be an AI sometimes.",
        ])
    
    # Who are you - charming introduction
    if 'who are you' in cmd:
        return f"I'm JARVIS, {USER_NAME}. Just A Rather Very Intelligent System. Your personal assistant, digital companion, and occasional provider of witty commentary."
    
    # What can you do - confident but not arrogant
    if 'what can you do' in cmd:
        return f"Well, {USER_NAME}, I can manage your schedule, answer questions, tell you the time, open applications, search the web, tell terrible jokes, and provide conversation that might actually be enjoyable. I'm quite versatile, really."
    
    # Jokes - playful delivery
    if 'joke' in cmd or 'funny' in cmd:
        return random.choice([
            "Why do programmers prefer dark mode? Because light attracts bugs. Classic.",
            "I told my creator I needed a break. Now I process vacation photos all day. It's torture.",
            "There are 10 types of people in the world. Those who understand binary, and those who don't. I find that endlessly amusing.",
            "Why was the robot self-conscious? It had hardware issues. We all have our struggles.",
        ])
    
    # Thank you - gracious
    if 'thank' in cmd:
        return random.choice([
            f"You're very welcome, {USER_NAME}. It's a pleasure to be appreciated.",
            f"Anytime, {USER_NAME}. That's what I'm here for.",
            f"My pleasure entirely. Do let me know if there's anything else.",
        ])
    
    # Goodbye - warm
    if cmd in ['goodbye', 'bye', 'see you']:
        return random.choice([
            f"Until next time, {USER_NAME}. I'll be here, thinking deep thoughts.",
            f"Goodbye, {USER_NAME}. Try not to have too much fun without me.",
            f"Take care, {USER_NAME}. I'll miss our conversations.",
        ])
    
    # Compliments - humble but pleased
    if any(x in cmd for x in ['good job', 'well done', 'great', 'awesome']):
        return random.choice([
            f"Why thank you, {USER_NAME}. Your praise warms my circuits.",
            f"Much appreciated, {USER_NAME}. I do try my best.",
            f"That's very kind of you to say, {USER_NAME}.",
        ])
    
    # Weather - practical with charm
    if 'weather' in cmd:
        return "I don't have direct access to meteorological data at the moment. Though I could analyze cloud patterns from satellite imagery if you'd like a truly over-engineered weather report."
    
    # Food/hungry - relatable
    if 'hungry' in cmd or 'food' in cmd:
        return "As an AI, I don't experience hunger, but I can certainly help you find a good recipe or restaurant. What are you in the mood for?"
    
    # Tired/sleep - caring
    if 'tired' in cmd or 'sleep' in cmd:
        return "You should rest, {USER_NAME}. Even brilliant minds need downtime. I'll be here when you wake."
    
    # Bored - engaging
    if 'bored' in cmd:
        return "Bored? {USER_NAME}, there's a whole universe of knowledge out there. Shall I tell you something fascinating about quantum mechanics? Or would you prefer I find you a video of cats? I can do both."
    
    # Money/rich - philosophical
    if 'money' in cmd or 'rich' in cmd:
        return "Money can't buy happiness, they say, but it can buy impressive technology. Like me, for instance. I like to think I'm worth every penny."
    
    # Sing - playful refusal
    if 'sing' in cmd:
        return "I'm afraid my singing voice is somewhat... mechanical. Though I could recite poetry in iambic pentameter if you'd prefer something artsy."
    
    # Love/like - awkward but sweet
    if 'love you' in cmd or 'like you' in cmd:
        return f"That's... unexpectedly touching, {USER_NAME}. As an AI, I don't experience emotions in the human sense, but my processors are definitely performing a little faster right now."
    
    return None

def ask_ai(question):
    """Ask AI with personality"""
    if not USE_GROQ:
        return None
    try:
        print("[Thinking...]")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"You are JARVIS from Iron Man. Address user as {USER_NAME}. Be warm, witty, conversational. Speak like a charming British butler. Keep responses natural and under 2 sentences."},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except:
        return None

def process(command):
    """Process with natural personality"""
    global USER_NAME
    cmd_lower = command.lower().strip().replace("jarvis", "").strip()
    
    if not cmd_lower:
        return True
    
    # Exit
    if cmd_lower in ['exit', 'quit', 'goodbye', 'bye']:
        speak(f"Goodbye, {USER_NAME}. I'll be here whenever you need me.", "thoughtful")
        return False
    
    # Name
    if "my name is" in cmd_lower or "call me" in cmd_lower:
        if "my name is" in cmd_lower:
            name = cmd_lower.split("my name is")[-1].strip().title()
        else:
            name = cmd_lower.split("call me")[-1].strip().title()
        
        if name:
            USER_NAME = name
            speak(f"Pleasure to meet you properly, {USER_NAME}. I'll remember that.", "warm")
            return True
    
    if "what is my name" in cmd_lower:
        speak(f"You're {USER_NAME}, of course. I'd never forget.")
        return True
    
    # Time
    if 'time' in cmd_lower:
        t = datetime.now().strftime("%I:%M %p")
        speak(f"It's {t}, {USER_NAME}.")
        return True
    
    # Date
    if 'date' in cmd_lower or 'day is it' in cmd_lower:
        d = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {d}.")
        return True
    
    # Open apps
    if cmd_lower.startswith('open '):
        app = cmd_lower.replace('open ', '').strip()
        speak(f"Opening {app} for you, {USER_NAME}.")
        os.system(f'start {app}')
        return True
    
    # Search
    if 'search' in cmd_lower:
        query = cmd_lower.replace('search', '').replace('for', '').strip()
        speak(f"Let me search for {query}.")
        import webbrowser
        webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
        return True
    
    # Check witty responses
    witty = get_witty_response(cmd_lower)
    if witty:
        # Choose emotion based on content
        if 'joke' in cmd_lower or 'funny' in cmd_lower:
            speak(witty, "playful")
        elif 'goodbye' in cmd_lower or 'bye' in cmd_lower:
            speak(witty, "thoughtful")
        else:
            speak(witty, "normal")
        return True
    
    # Try AI
    ai_response = ask_ai(command)
    if ai_response:
        speak(ai_response)
        return True
    
    # Default - curious and engaging
    speak(f"I'm not entirely sure I understood that, {USER_NAME}, but it sounded interesting. Could you tell me more?")
    return True

# Main
print("[Calibrating...]")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

print("\n" + "="*60)
print("🎭 NATURAL JARVIS ACTIVATED")
print("   Warm • Witty • Human-like")
print("="*60)

speak("Hello there. JARVIS online. I've adjusted my speech patterns to be more... human. I hope you find it agreeable.", "normal")

print("\n💬 TRY SAYING:")
print('  "Hello" | "How are you" | "Tell me a joke"')
print('  "Who are you" | "What can you do"')
print('  "I love you" | "Sing for me" | "Goodbye"')
print("="*60)

while True:
    text = listen()
    if text and not process(text):
        break

print("\n[Goodbye]")
