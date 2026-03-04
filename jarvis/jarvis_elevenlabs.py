#!/usr/bin/env python3
"""
JARVIS - ElevenLabs Voice Edition
Uses ElevenLabs AI for realistic JARVIS voice
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os
import sys

print("="*60)
print("JARVIS - ELEVENLABS VOICE EDITION")
print("="*60)

# User info
USER_NAME = "sir"

# Setup speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

# ElevenLabs setup
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
USE_ELEVENLABS = False
elevenlabs_client = None

if ELEVENLABS_API_KEY:
    try:
        from elevenlabs import ElevenLabs, VoiceSettings
        elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        USE_ELEVENLABS = True
        print("[✓] ElevenLabs connected - JARVIS voice ready!")
    except ImportError:
        print("[!] Install ElevenLabs: pip install elevenlabs")
    except Exception as e:
        print(f"[!] ElevenLabs error: {e}")

# Fallback TTS setup
print("[INIT] Configuring backup voice...")
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 0.9)

# Try to find best available local voice
voices = engine.getProperty('voices')
selected_voice = None
for voice in voices:
    voice_name = voice.name.lower()
    if any(x in voice_name for x in ['british', 'uk', 'george', 'david']):
        if 'female' not in voice_name:
            selected_voice = voice.id
            break
if selected_voice:
    engine.setProperty('voice', selected_voice)

# Groq setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
USE_GROQ = False
if GROQ_API_KEY:
    try:
        import groq
        groq_client = groq.Client(api_key=GROQ_API_KEY)
        USE_GROQ = True
    except:
        pass

def speak(text):
    """Speak with ElevenLabs or fallback"""
    global USER_NAME
    text = text.replace("{name}", USER_NAME)
    
    print(f"\n🔊 JARVIS: \"{text}\"")
    
    # Try ElevenLabs first
    if USE_ELEVENLABS and elevenlabs_client:
        try:
            from elevenlabs import VoiceSettings
            
            # Generate speech with JARVIS-like voice
            # Using voice from: https://elevenlabs.io/app/voice-library?voiceId=jMmnqbNMAz7cuNoKGfIb
            audio = elevenlabs_client.generate(
                text=text,
                voice="jMmnqbNMAz7cuNoKGfIb",  # Specific JARVIS-like voice
                model="eleven_monolingual_v1",
                voice_settings=VoiceSettings(
                    stability=0.5,  # Balanced
                    similarity_boost=0.75,  # Clear but natural
                    style=0.3,  # Slight emphasis
                    use_speaker_boost=True
                )
            )
            
            # Play audio
            from elevenlabs import play
            play(audio)
            return
            
        except Exception as e:
            print(f"[ElevenLabs error, using backup: {e}]")
    
    # Fallback to local TTS
    try:
        local_engine = pyttsx3.init()
        if selected_voice:
            local_engine.setProperty('voice', selected_voice)
        local_engine.setProperty('rate', 160)
        local_engine.setProperty('volume', 0.9)
        local_engine.say(text)
        local_engine.runAndWait()
    except Exception as e:
        print(f"[Voice error: {e}]")

def listen():
    """Listen for command"""
    with microphone as source:
        print("\n[LISTENING...]")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("[Processing...]")
            text = recognizer.recognize_google(audio)
            print(f"[You: '{text}']")
            return text
        except:
            return None

def ask_groq(question):
    """Ask Groq AI"""
    if not USE_GROQ:
        return None
    try:
        print("[🧠 Analyzing...]")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are JARVIS from Iron Man. Be sophisticated, helpful, and concise."},
                {"role": "user", "content": question}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except:
        return None

def process(command):
    """Process command"""
    global USER_NAME
    cmd_lower = command.lower().strip().replace("jarvis", "").strip()
    
    if not cmd_lower:
        return True
    
    # Exit
    if cmd_lower in ['exit', 'quit', 'goodbye', 'bye']:
        speak("As you wish, {name}. Shutting down. It has been a pleasure.")
        return False
    
    # Name handling
    if "my name is" in cmd_lower or "call me" in cmd_lower:
        if "my name is" in cmd_lower:
            name = cmd_lower.split("my name is")[-1].strip().title()
        else:
            name = cmd_lower.split("call me")[-1].strip().title()
        
        if name:
            USER_NAME = name
            speak(f"Very good, {USER_NAME}. I shall address you accordingly.")
            return True
    
    if "what is my name" in cmd_lower:
        speak(f"You are {USER_NAME}, of course.")
        return True
    
    # Time/Date
    if 'time' in cmd_lower:
        t = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {t}, {USER_NAME}.")
        return True
    
    if 'date' in cmd_lower:
        d = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {d}, {USER_NAME}.")
        return True
    
    # Open apps
    if cmd_lower.startswith('open '):
        app = cmd_lower.replace('open ', '').strip()
        speak(f"Opening {app}, {USER_NAME}.")
        os.system(f'start {app}')
        return True
    
    # Search
    if 'search' in cmd_lower:
        query = cmd_lower.replace('search', '').replace('for', '').strip()
        speak(f"Searching for {query}.")
        import webbrowser
        webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
        return True
    
    # Greetings
    if any(x in cmd_lower for x in ['hello', 'hi', 'hey']):
        speak(f"Hello, {USER_NAME}. JARVIS at your service. How may I be of assistance?")
        return True
    
    if 'how are you' in cmd_lower:
        speak(f"All systems are functioning at optimal levels, thank you for asking, {USER_NAME}.")
        return True
    
    if 'who are you' in cmd_lower:
        speak(f"I am JARVIS - Just A Rather Very Intelligent System. I am your personal AI assistant, {USER_NAME}.")
        return True
    
    # Status
    if 'status' in cmd_lower:
        speak(f"All systems nominal. I am operating at full capacity and ready to assist you, {USER_NAME}.")
        return True
    
    # Use AI
    ai_response = ask_groq(command)
    if ai_response:
        speak(ai_response)
        return True
    
    # Default
    speak(f"I apologize, {USER_NAME}. I am not certain I understood your request. Could you please rephrase?")
    return True

# Main
print("[Calibrating microphone...]")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

print("\n" + "="*60)
if USE_ELEVENLABS:
    print("🎬 JARVIS WITH REALISTIC AI VOICE (ElevenLabs)")
else:
    print("🎬 JARVIS MOVIE VOICE MODE")
    print("   For realistic AI voice, get ElevenLabs API key:")
    print("   https://elevenlabs.io → Sign up → Get API key")
    print("   Then run: setx ELEVENLABS_API_KEY your-key")
print("="*60)

if USE_ELEVENLABS:
    speak("Good day, {name}. JARVIS online with enhanced vocal capabilities. I am ready to assist you.")
else:
    speak("Good day, {name}. JARVIS is now online and ready to assist you.")

print("\n💡 TRY SAYING:")
print('  "Hello" | "What time is it" | "My name is Master Brown"')
print('  "Open notepad" | "Who are you" | "Exit"')
print("="*60)

while True:
    text = listen()
    if text and not process(text):
        break

print("\n[Shutdown complete]")
