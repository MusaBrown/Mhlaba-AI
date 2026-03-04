"""
Voice Recognition Module
Handles speech-to-text functionality
"""
import asyncio
import speech_recognition as sr
from config import Config


class VoiceListener:
    """Listens for voice commands and converts to text"""
    
    def __init__(self, config: Config):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibrate for ambient noise
        self._calibrate()
        
    def _calibrate(self):
        """Calibrate microphone for ambient noise"""
        print("[MIC] Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        # Set a minimum threshold to avoid being too sensitive
        min_threshold = 1500
        if self.recognizer.energy_threshold < min_threshold:
            self.recognizer.energy_threshold = min_threshold
        print(f"[MIC] Microphone calibrated (threshold: {self.recognizer.energy_threshold})")
        
        # Set recognition parameters
        self.recognizer.energy_threshold = self.config.energy_threshold
        self.recognizer.pause_threshold = self.config.pause_threshold
        self.recognizer.phrase_threshold = self.config.phrase_threshold
        
    async def listen_for_command(self, timeout: int = 5) -> str:
        """Listen for a voice command and return the text"""
        try:
            with self.microphone as source:
                print("[MIC] Listening for speech... (say something)")
                # Listen with timeout
                audio = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                )
                
            print("[MIC] Audio detected! Processing...")
            
            # Try multiple recognition services
            text = await self._recognize_with_fallback(audio)
            
            if text:
                return text.lower()
            return None
            
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"Listening error: {e}")
            return None
            
    async def _recognize_with_fallback(self, audio) -> str:
        """Try multiple speech recognition services"""
        # Try Google Speech Recognition first (most accurate, requires internet)
        try:
            print("[MIC] Sending to Google Speech Recognition...")
            text = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.recognizer.recognize_google(audio)
            )
            print(f"[MIC] Google heard: '{text}'")
            return text
        except sr.UnknownValueError:
            print("[MIC] Could not understand audio (Google)")
        except sr.RequestError as e:
            print(f"[WARN] Google Speech error: {e}")
            
        # Fallback to Sphinx (offline, less accurate)
        try:
            print("[MIC] Trying offline recognition (Sphinx)...")
            text = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.recognizer.recognize_sphinx(audio)
            )
            print(f"[MIC] Sphinx heard: '{text}'")
            return text
        except Exception as e:
            print(f"[MIC] Sphinx error: {e}")
            pass
            
        return None
        
    async def listen_continuous(self, callback):
        """Continuously listen for commands"""
        while True:
            command = await self.listen_for_command()
            if command:
                await callback(command)
            await asyncio.sleep(0.1)
