"""
Text-to-Speech Module
Handles speech synthesis
"""
import asyncio
import pyttsx3
from pathlib import Path
from config import Config


class VoiceSpeaker:
    """Converts text to speech"""
    
    def __init__(self):
        self.engine = None
        self._init_engine()
        
    def _init_engine(self):
        """Initialize the TTS engine"""
        try:
            self.engine = pyttsx3.init()
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            
            # Try to find a good English voice
            selected_voice = None
            for voice in voices:
                if 'english' in voice.name.lower() or 'en-us' in voice.id.lower():
                    selected_voice = voice.id
                    break
                    
            if selected_voice:
                self.engine.setProperty('voice', selected_voice)
                
            # Set speech rate
            self.engine.setProperty('rate', 175)
            
            # Set volume
            self.engine.setProperty('volume', 0.9)
            
            print("[VOICE] Voice engine initialized")
            
        except Exception as e:
            print(f"[WARN] Could not initialize voice engine: {e}")
            self.engine = None
            
    async def speak(self, text: str):
        """Speak the given text"""
        if not text:
            return
            
        print(f"[SPEAK] {text}")
        
        if self.engine:
            try:
                # Run TTS in executor to not block
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    self._speak_sync,
                    text
                )
            except Exception as e:
                print(f"TTS error: {e}")
        else:
            print(f"[VOICE]: {text}")
            
    def _speak_sync(self, text: str):
        """Synchronous speech (runs in thread)"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
            # Reinitialize engine on error
            self._init_engine()
            
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        if self.engine:
            return [(v.id, v.name) for v in self.engine.getProperty('voices')]
        return []
        
    def set_voice(self, voice_id: str):
        """Set a specific voice"""
        if self.engine:
            self.engine.setProperty('voice', voice_id)
            
    def set_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        if self.engine:
            self.engine.setProperty('rate', rate)
