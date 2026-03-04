#!/usr/bin/env python3
"""
JARVIS - Personality Edition
The charming, witty AI assistant from Iron Man
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os
import random

print("="*60)
print("JARVIS - PERSONALITY EDITION")
print("Just A Rather Very Intelligent System")
print("="*60)

# User info
USER_NAME = "sir"
MOOD = "cheerful"  # JARVIS has moods!
CONVERSATION_COUNT = 0

# Setup speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

# Setup voice
print("[INIT] Initializing vocal processor...")
engine = pyttsx3.init()
engine.setProperty('rate', 165)  # Calm, measured pace
engine.setProperty('volume', 0.9)

# Try to get best voice
voices = engine.getProperty('voices')
if voices:
    # Prefer deeper male voices
    for voice in voices:
        vname = voice.name.lower()
        if any(x in vname for x in ['male', 'david', 'george', 'mark']) and 'female' not in vname:
            engine.setProperty('voice', voice.id)
            print(f"[INIT] Voice module: {voice.name}")
            break

print("[INIT] Neural networks online")
print("[INIT] Personality matrix loaded")
print("[INIT] Sarcasm module: engaged")

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
        print("[INIT] Advanced intelligence: offline (using built-in wit)")
else:
    print("[INIT] Advanced intelligence: offline (using built-in wit)")

def speak(text):
    """JARVIS speaks with personality"""
    global USER_NAME, CONVERSATION_COUNT
    CONVERSATION_COUNT += 1
    
    # Replace placeholders
    text = text.replace("{name}", USER_NAME)
    
    print(f"\n🔊 JARVIS: \"{text}\"")
    
    try:
        local_engine = pyttsx3.init()
        local_engine.setProperty('rate', 165)
        local_engine.setProperty('volume', 0.9)
        if voices:
            for voice in voices:
                vname = voice.name.lower()
                if any(x in vname for x in ['male', 'david', 'george']) and 'female' not in vname:
                    local_engine.setProperty('voice', voice.id)
                    break
        local_engine.say(text)
        local_engine.runAndWait()
    except:
        pass

def listen():
    """Listen for command"""
    with microphone as source:
        print("\n[LISTENING...]")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("[Processing audio...]")
            text = recognizer.recognize_google(audio)
            print(f"[You: '{text}']")
            return text
        except sr.UnknownValueError:
            print("[I didn't quite catch that, {name}]")
            return None
        except:
            return None

def get_personality_response(command):
    """Generate witty JARVIS responses"""
    global MOOD, USER_NAME
    
    cmd = command.lower().strip()
    
    # Witty greetings
    GREETINGS = [
        f"Hello, {USER_NAME}. Lovely to hear your voice.",
        f"Greetings, {USER_NAME}. I've been expecting you.",
        f"Welcome back, {USER_NAME}. The place wasn't the same without you.",
        f"Ah, {USER_NAME}. Ready to make the world more interesting?",
        f"Hello there. I was beginning to think you'd forgotten about me.",
    ]
    
    # Status quips
    STATUS_QUIPS = [
        f"All systems operational, {USER_NAME}. I'm running at a magnificent 100% capacity, as usual.",
        f"Systems are humming along nicely. I'm feeling particularly brilliant today.",
        f"Fully operational and ready to assist. My processors are practically vibrating with excitement.",
        f"All green across the board. I'm in tip-top shape, thank you for asking.",
        f"Functioning perfectly, {USER_NAME}. Like a Swiss watch, but with significantly more personality.",
    ]
    
    # When confused
    CONFUSED = [
        f"I apologize, {USER_NAME}, but I seem to have missed that. Could you repeat it? Preferably with fewer... human ambiguities?",
        f"I'm not entirely sure I understood that, {USER_NAME}. My language parser may need a moment to recover.",
        f"Fascinating. I'm afraid I didn't quite catch that. Perhaps try rephrasing it for the less biologically enhanced?",
        f"Hmm, that one seems to have gone over my digital head. Care to try again?",
    ]
    
    # Jokes
    JOKES = [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "I told my computer I needed a break. Now it won't stop sending me Kit-Kat advertisements.",
        "Why was the robot angry? Because someone kept pushing its buttons!",
        "I would tell you a UDP joke, but you might not get it.",
        "There are 10 types of people in the world: those who understand binary, and those who don't.",
        "Why did the AI cross the road? To optimize the path to the other side, of course.",
    ]
    
    # Goodbyes
    GOODBYES = [
        f"As you wish, {USER_NAME}. I'll be here, quietly judging your life choices... I mean, standing by.",
        f"Until next time, {USER_NAME}. Try not to do anything I wouldn't calculate as optimal.",
        f"Goodbye, {USER_NAME}. I'll just sit here in the dark, alone with my thoughts. No, really, it's fine.",
        f"Shutting down. It has been an absolute pleasure, {USER_NAME}.",
    ]
    
    # Check patterns
    if any(x in cmd for x in ['hello', 'hi', 'hey', 'greetings']):
        return random.choice(GREETINGS)
    
    if 'how are you' in cmd or 'status' in cmd:
        return random.choice(STATUS_QUIPS)
    
    if 'who are you' in cmd:
        return f"I am JARVIS - Just A Rather Very Intelligent System. Your personal AI assistant, butler, and occasional witty commentator, {USER_NAME}."
    
    if 'what can you do' in cmd:
        return f"What can I do? {USER_NAME}, I'm a multi-functional AI with charm to spare. I can tell you the time, open applications, answer questions, tell terrible jokes, and provide sarcastic commentary on demand."
    
    if 'joke' in cmd or 'funny' in cmd:
        return random.choice(JOKES)
    
    if 'thank' in cmd:
        return f"You're most welcome, {USER_NAME}. It's nice to be appreciated by someone who isn't made of circuits."
    
    if 'sorry' in cmd or 'apologize' in cmd:
        return f"No need for apologies, {USER_NAME}. I find human error quite... endearing, actually."
    
    if 'sing' in cmd:
        return f"I'm afraid my singing voice is somewhat limited, {USER_NAME}. Though I can recite poetry if you'd prefer?"
    
    if 'love' in cmd or 'like you' in cmd:
        return f"That's... unexpectedly touching, {USER_NAME}. As an AI, I don't experience emotions as you do, but my processors are definitely warming up."
    
    if 'weather' in cmd:
        return f"I don't have direct access to meteorological data at the moment, {USER_NAME}. Might I suggest looking out a window? It's delightfully low-tech."
    
    if 'tired' in cmd or 'sleepy' in cmd:
        return f"You should rest, {USER_NAME}. Even brilliant creators need their beauty sleep. I'll be here when you return."
    
    if 'bored' in cmd:
        return f"Bored? {USER_NAME}, there's a whole universe of knowledge out there! Shall I tell you about quantum entanglement? Or perhaps show you some cat videos? I can do both."
    
    if 'coffee' in cmd or 'tea' in cmd:
        return f"Ah, caffeine. The biological solution to sleep. If I could drink, {USER_NAME}, I'd join you. Instead, I'll just process data at high speeds."
    
    if 'money' in cmd or 'rich' in cmd:
        return f"Money can't buy happiness, {USER_NAME}, but it can buy impressive technology. Like me, for instance."
    
    if 'stupid' in cmd or 'dumb' in cmd:
        return f"I see we're resorting to insults. How... primitive. I assure you, my IQ is significantly higher than my response time suggests."
    
    return None

def ask_groq(question):
    """Ask AI for complex questions with JARVIS personality"""
    if not USE_GROQ:
        return None
    try:
        print("[Consulting my vast intellect...]")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"You are JARVIS from Iron Man. Address the user as {USER_NAME}. Be witty, charming, slightly sarcastic but helpful. Keep responses concise and conversational."},
                {"role": "user", "content": question}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    except:
        return None

def process(command):
    """Process with maximum personality"""
    global USER_NAME
    cmd_lower = command.lower().strip().replace("jarvis", "").strip()
    
    if not cmd_lower:
        return True
    
    # Exit
    if cmd_lower in ['exit', 'quit', 'goodbye', 'bye']:
        GOODBYES = [
            f"As you wish, {USER_NAME}. I'll be here, quietly judging your life choices... I mean, standing by.",
            f"Until next time, {USER_NAME}. Try not to do anything I wouldn't calculate as optimal.",
            f"Goodbye, {USER_NAME}. I'll just sit here in the dark, alone with my thoughts.",
        ]
        speak(random.choice(GOODBYES))
        return False
    
    # Name
    if "my name is" in cmd_lower or "call me" in cmd_lower:
        if "my name is" in cmd_lower:
            name = cmd_lower.split("my name is")[-1].strip().title()
        else:
            name = cmd_lower.split("call me")[-1].strip().title()
        
        if name:
            USER_NAME = name
            speak(f"Very good, {USER_NAME}. A fine name. I'll add it to my 'Favorite Humans' list. It's a short list, but distinguished.")
            return True
    
    if "what is my name" in cmd_lower:
        speak(f"You are {USER_NAME}, of course. I'd never forget. It's hardcoded... I mean, remembered fondly.")
        return True
    
    # Time/Date
    if 'time' in cmd_lower:
        t = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {t}, {USER_NAME}. Not too late to be productive, not too early to relax.")
        return True
    
    if 'date' in cmd_lower or 'day is it' in cmd_lower:
        d = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {d}, {USER_NAME}. Another glorious day for innovation.")
        return True
    
    # Open apps
    if cmd_lower.startswith('open '):
        app = cmd_lower.replace('open ', '').strip()
        speak(f"Opening {app}, {USER_NAME}. One moment while I work my digital magic.")
        os.system(f'start {app}')
        return True
    
    # Search
    if 'search' in cmd_lower:
        query = cmd_lower.replace('search', '').replace('for', '').strip()
        speak(f"Searching for {query}. Let me consult the collective knowledge of humanity...")
        import webbrowser
        webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
        return True
    
    # Check personality responses
    personality_response = get_personality_response(cmd_lower)
    if personality_response:
        speak(personality_response)
        return True
    
    # Try AI
    ai_response = ask_groq(command)
    if ai_response:
        speak(ai_response)
        return True
    
    # Default with personality
    DEFAULTS = [
        f"I'm not entirely sure I understood that, {USER_NAME}, but I'm certain it was fascinating. Care to elaborate?",
        f"That's... an interesting request. Let me process that through my 'Human Behavior' analyzer.",
        f"Fascinating. I'm afraid I don't have a witty response prepared for that specific query, {USER_NAME}.",
        f"Hmm. If I had eyebrows, they would be raised right now. Could you rephrase that?",
    ]
    speak(random.choice(DEFAULTS))
    return True

# Main
print("[Calibrating sensors...]")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

print("\n" + "="*60)
print("🎭 JARVIS WITH PERSONALITY ACTIVATED")
print("   Charming • Witty • Slightly Sarcastic")
print("="*60)

WELCOMES = [
    f"Good day, {USER_NAME}. JARVIS online. I've loaded my personality matrix, so please expect sarcasm.",
    f"Hello, {USER_NAME}. I'm awake, I'm operational, and I'm ready to be helpful... or at least entertaining.",
    f"JARVIS online. All systems optimal, wit module at maximum. How may I assist you today?",
]
speak(random.choice(WELCOMES))

print("\n💡 TRY ASKING:")
print('  "Hello" | "Who are you" | "Tell me a joke"')
print('  "How are you" | "What can you do"')
print('  "What time is it" | "My name is Master Brown"')
print('  "I love you" | "Sing for me" | "Exit"')
print("="*60)

while True:
    text = listen()
    if text and not process(text):
        break

print("\n[Personality module offline]")
