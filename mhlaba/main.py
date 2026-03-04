#!/usr/bin/env python3
"""
MHLABA - My Helpful Learning Assistant & Brilliant Aid
A voice-activated AI assistant for Windows
"""

import asyncio
import sys
import signal
import os
from pathlib import Path
from datetime import datetime

from voice_listener import VoiceListener
from voice_speaker import VoiceSpeaker
from ai_brain import AIBrain
from document_handler import DocumentHandler
from system_executor import SystemExecutor
from screen_reader import ScreenReader
from config import Config


class Mhlaba:
    """Main MHLABA Assistant Class"""
    
    def __init__(self):
        print("[MHLABA] Initializing MHLABA...")
        self.config = Config()
        self.speaker = VoiceSpeaker()
        self.brain = AIBrain()
        self.doc_handler = DocumentHandler()
        self.executor = SystemExecutor()
        self.screen_reader = ScreenReader()
        self.listener = VoiceListener(self.config)
        self.running = False
        self.wake_word = "mhlaba"
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print("\n[MHLABA] Shutting down MHLABA...")
        self.running = False
        
    async def startup(self):
        """Initialize all components"""
        await self.speaker.speak("MHLABA online. Systems operational. How may I assist you today?")
        
    async def process_command(self, command: str):
        """Process a voice command"""
        command = command.lower().strip()
        print(f"[CMD] {command}")
        
        # Check for system commands first
        if await self._handle_system_commands(command):
            return
            
        # Check for document operations
        if await self._handle_document_commands(command):
            return
            
        # Check for screen reading operations
        if await self._handle_screen_commands(command):
            return
            
        # Check for document discussion mode
        if self.brain.document_discussion_mode:
            response = await self.brain.discuss_document(command)
            print(f"[MHLABA] {response}")
            await self.speaker.speak(response)
            return
            
        # Default: Use AI brain for conversation
        response = await self.brain.generate_response(command)
        print(f"[MHLABA] {response}")
        await self.speaker.speak(response)
        
    async def _handle_system_commands(self, command: str) -> bool:
        """Handle system-level commands"""
        # Time and date
        if "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
            await self.speaker.speak(response)
            return True
            
        if "date" in command or "day" in command:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            response = f"Today is {current_date}"
            await self.speaker.speak(response)
            return True
            
        # Open applications
        if command.startswith("open") or command.startswith("launch"):
            app_name = command.replace("open", "").replace("launch", "").strip()
            result = self.executor.open_application(app_name)
            await self.speaker.speak(result)
            return True
            
        # Web search
        if "search" in command or "look up" in command:
            query = command.replace("search", "").replace("look up", "").replace("for", "").strip()
            result = self.executor.web_search(query)
            await self.speaker.speak(f"Searching for {query}")
            return True
            
        # System info
        if "system info" in command or "computer info" in command:
            info = self.executor.get_system_info()
            await self.speaker.speak(info)
            return True
            
        return False
        
    async def _handle_document_commands(self, command: str) -> bool:
        """Handle document-related commands"""
        # Read document
        if "read" in command and ("file" in command or "document" in command):
            # Extract filename from command
            words = command.split()
            for i, word in enumerate(words):
                if word in ["read", "file", "document"]:
                    continue
                # Try to find the file
                potential_file = " ".join(words[i:])
                content = self.doc_handler.read_document(potential_file)
                if content:
                    await self.speaker.speak(f"Here's the content of {potential_file}")
                    print(f"\n{'='*50}\n{content[:500]}...\n{'='*50}")
                    # Summarize long content
                    if len(content) > 300:
                        summary = await self.brain.summarize(content[:2000])
                        await self.speaker.speak(f"Summary: {summary}")
                    else:
                        await self.speaker.speak(content)
                    return True
                    
        # List files in directory
        if "list files" in command or "show files" in command:
            files = self.doc_handler.list_files()
            if files:
                file_list = ", ".join(files[:10])
                response = f"Files in current directory: {file_list}"
                if len(files) > 10:
                    response += f" and {len(files) - 10} more"
            else:
                response = "No files found in the current directory"
            await self.speaker.speak(response)
            return True
            
        # Stop discussing document
        if any(x in command for x in ["stop discussing", "close document", "end discussion"]):
            self.brain.clear_active_document()
            await self.speaker.speak("Document discussion ended. What else can I help you with?")
            return True
            
        return False
        
    async def _handle_screen_commands(self, command: str) -> bool:
        """Handle screen reading commands"""
        # Read screen / What's on my screen
        if any(x in command for x in ["read screen", "what's on my screen", "whats on my screen", 
                                       "describe screen", "see my screen", "look at screen",
                                       "capture screen", "take screenshot"]):
            await self.speaker.speak("Capturing your screen now.")
            print("[SCREEN] Capturing...")
            
            screen_data = self.screen_reader.read_screen()
            
            if not screen_data['success']:
                error_msg = f"I couldn't capture your screen: {screen_data.get('error', 'Unknown error')}"
                print(f"[SCREEN ERROR] {error_msg}")
                await self.speaker.speak(error_msg)
                return True
                
            # Display results
            analysis = screen_data['analysis']
            print(f"\n{'='*50}")
            print(f"SCREEN CAPTURE: {analysis['content_type'].upper()}")
            print(f"Words: {analysis['word_count']}, Lines: {analysis['line_count']}")
            print(f"Screenshot saved to: {screen_data['screenshot_path']}")
            print(f"{'='*50}")
            print(f"KEY ELEMENTS:")
            for elem in analysis['key_elements'][:5]:
                print(f"  • {elem}")
            print(f"{'='*50}")
            print(f"EXTRACTED TEXT (first 500 chars):\n{screen_data['text'][:500]}...")
            print(f"{'='*50}\n")
            
            # Provide spoken summary
            content_type = analysis['content_type']
            word_count = analysis['word_count']
            
            summary = f"I've captured your screen. I can see {content_type} content with approximately {word_count} words."
            
            if analysis['key_elements']:
                summary += f" Key elements include: {', '.join(analysis['key_elements'][:3])}."
                
            await self.speaker.speak(summary)
            
            # If AI provider is available, provide deeper analysis
            if self.brain.provider in ["openai", "anthropic"]:
                await self.speaker.speak("Analyzing the content for you.")
                description = self.screen_reader.describe_for_ai(screen_data)
                ai_analysis = await self.brain.analyze_screen(description)
                print(f"\n[AI ANALYSIS]\n{ai_analysis}\n")
                await self.speaker.speak(ai_analysis[:300])
                
            return True
            
        return False
        
    async def run(self):
        """Main loop"""
        await self.startup()
        self.running = True
        
        print("\n" + "="*50)
        print("MHLABA IS READY")
        print("="*50)
        print(f"VOICE MODE: Say '{self.wake_word.upper()}' followed by your command")
        print("TEXT MODE: Type your command below and press Enter")
        print("Type 'exit' to quit")
        print("="*50)
        print("\n[INFO] Listening in background... Say 'Mhlaba hello' or type below:\n")
        
        # Start listening in background
        listen_task = asyncio.create_task(self._listen_loop())
        
        # Also accept text input
        while self.running:
            try:
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: input("\nYou: ")
                )
                
                if user_input.lower() in ['exit', 'quit', 'goodbye', 'bye']:
                    await self.speaker.speak("Goodbye. MHLABA standing by.")
                    self.running = False
                    break
                    
                if user_input.strip():
                    await self.process_command(user_input)
                    
            except Exception as e:
                print(f"Error: {e}")
                
        listen_task.cancel()
        
    async def _listen_loop(self):
        """Background voice listening loop"""
        while self.running:
            try:
                command = await self.listener.listen_for_command()
                if command:
                    print(f"\n[VOICE] Heard: '{command}'")
                    if self.wake_word in command.lower() or not self.config.use_wake_word:
                        # Remove wake word and process
                        clean_command = command.lower().replace(self.wake_word, "").strip()
                        print(f"[VOICE] Processing command: '{clean_command}'")
                        if clean_command:
                            await self.process_command(clean_command)
                    else:
                        print(f"[VOICE] Wake word '{self.wake_word}' not detected. Ignored.")
                        print(f"[VOICE] Try saying: 'Mhlaba what time is it'")
            except Exception as e:
                print(f"[VOICE ERROR] {e}")
            await asyncio.sleep(0.5)


async def main():
    """Entry point"""
    mhlaba = Mhlaba()
    await mhlaba.run()


if __name__ == "__main__":
    asyncio.run(main())
