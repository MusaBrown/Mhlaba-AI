#!/usr/bin/env python3
"""
JARVIS - Working Voice Version
Uses blocking calls like the diagnostic
"""

import speech_recognition as sr
from voice_speaker import VoiceSpeaker
from ai_brain import AIBrain
from document_handler import DocumentHandler
from system_executor import SystemExecutor
from datetime import datetime
import threading
import time


class JarvisWorking:
    def __init__(self):
        print("[JARVIS] Initializing...")
        
        # Voice components
        self.speaker = VoiceSpeaker()
        self.brain = AIBrain()
        self.docs = DocumentHandler()
        self.executor = SystemExecutor()
        
        # Speech recognition setup (like diagnostic)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Settings that worked in diagnostic
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.pause_threshold = 1.0
        
        self.running = True
        self.listen_mode = True  # Toggle between listen and text
        
    def run(self):
        """Main run loop"""
        # Calibrate once at start
        print("[MIC] Calibrating... please wait...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"[MIC] Ready! Threshold: {self.recognizer.energy_threshold}")
        
        # Startup message
        self._speak("JARVIS online and ready")
        
        print("\n" + "="*60)
        print("JARVIS IS READY")
        print("="*60)
        print("COMMANDS:")
        print("  [v] = Voice mode (say 'Jarvis' + command)")
        print("  [t] = Type command")
        print("  [q] = Quit")
        print("="*60)
        
        while self.running:
            print()
            choice = input("Choose [v]oice, [t]ype, or [q]uit: ").lower().strip()
            
            if choice == 'q':
                self._speak("Goodbye")
                break
            elif choice == 'v':
                self._listen_once()
            elif choice == 't':
                self._text_input()
            else:
                print("Invalid choice. Try v, t, or q.")
                
    def _listen_once(self):
        """Listen for one command (like diagnostic)"""
        print()
        print(">>> LISTENING - SPEAK NOW <<<")
        print("(Say: 'Jarvis what time is it')")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            print("[MIC] Audio captured! Processing...")
            
            # Try Google
            try:
                text = self.recognizer.recognize_google(audio)
                print(f">>> HEARD: '{text}' <<<")
                
                # Check for wake word
                if "jarvis" in text.lower():
                    command = text.lower().replace("jarvis", "").strip()
                    self._process_command(command)
                else:
                    print("[INFO] Say 'Jarvis' before your command")
                    
            except sr.UnknownValueError:
                print("[ERROR] Could not understand audio")
                self._speak("I did not understand. Please try again.")
            except sr.RequestError as e:
                print(f"[ERROR] Google API error: {e}")
                
        except sr.WaitTimeoutError:
            print("[ERROR] Timeout - no speech detected")
        except Exception as e:
            print(f"[ERROR] {e}")
            
    def _text_input(self):
        """Get text command"""
        print()
        command = input("Type your command: ").strip()
        if command:
            self._process_command(command)
            
    def _process_command(self, command: str):
        """Process a command"""
        command = command.lower().strip()
        print(f"[CMD] Processing: '{command}'")
        
        # Exit
        if command in ['exit', 'quit', 'goodbye', 'bye']:
            self._speak("Goodbye. JARVIS standing by.")
            self.running = False
            return
            
        # Time
        if "time" in command:
            t = datetime.now().strftime("%I:%M %p")
            response = f"The time is {t}"
            print(f"[JARVIS] {response}")
            self._speak(response)
            return
            
        # Date
        if "date" in command or "day" in command:
            d = datetime.now().strftime("%A, %B %d, %Y")
            response = f"Today is {d}"
            print(f"[JARVIS] {response}")
            self._speak(response)
            return
            
        # System info
        if "system info" in command:
            info = self.executor.get_system_info()
            print(f"\n{info}\n")
            self._speak("System information displayed on screen")
            return
            
        # List files
        if "list files" in command or "show files" in command:
            files = self.docs.list_files()
            response = f"Found {len(files)} files in current directory"
            print(f"Files: {files[:10]}")
            self._speak(response)
            return
            
        # Open app
        if command.startswith("open ") or command.startswith("launch "):
            app = command.replace("open ", "").replace("launch ", "").strip()
            result = self.executor.open_application(app)
            print(f"[JARVIS] {result}")
            self._speak(result)
            return
            
        # Read file
        if "read" in command:
            parts = command.split()
            for i, p in enumerate(parts):
                if p == "read" and i + 1 < len(parts):
                    filename = " ".join(parts[i+1:])
                    content = self.docs.read_document(filename)
                    if content:
                        preview = content[:300] + "..." if len(content) > 300 else content
                        print(f"\n--- {filename} ---")
                        print(preview)
                        print("---")
                        self._speak(f"Here is the content of {filename}")
                    else:
                        self._speak(f"Could not read {filename}")
                    return
                    
        # Default: AI conversation
        response = self.brain.generate_response(command)
        # Response is a coroutine, need to run it
        import asyncio
        response = asyncio.run(self.brain.generate_response(command))
        print(f"[JARVIS] {response}")
        self._speak(response)
        
    def _speak(self, text: str):
        """Speak text"""
        import asyncio
        asyncio.run(self.speaker.speak(text))


def main():
    jarvis = JarvisWorking()
    jarvis.run()


if __name__ == "__main__":
    main()
