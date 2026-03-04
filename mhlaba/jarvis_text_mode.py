#!/usr/bin/env python3
"""
JARVIS - Text Mode (No Microphone Required)
Type commands instead of speaking
"""

import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path

# Same imports as main.py
from voice_speaker import VoiceSpeaker
from ai_brain import AIBrain
from document_handler import DocumentHandler
from system_executor import SystemExecutor
from screen_reader import ScreenReader
from config import Config


class JarvisText:
    """JARVIS that uses text input instead of voice"""
    
    def __init__(self):
        print("[JARVIS] Initializing...")
        self.config = Config()
        self.speaker = VoiceSpeaker()
        self.brain = AIBrain()
        self.doc_handler = DocumentHandler()
        self.executor = SystemExecutor()
        self.screen_reader = ScreenReader()
        self.running = False
        
    async def startup(self):
        """Initialize all components"""
        await self.speaker.speak("JARVIS online. Text mode active. How may I assist you?")
        
    async def process_command(self, command: str):
        """Process a text command"""
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
            print(f"[JARVIS] {response}")
            await self.speaker.speak(response)
            return
            
        # Default: Use AI brain for conversation
        response = await self.brain.generate_response(command)
        print(f"[JARVIS] {response}")
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
            words = command.split()
            for i, word in enumerate(words):
                if word in ["read", "file", "document"]:
                    continue
                potential_file = " ".join(words[i:])
                content = self.doc_handler.read_document(potential_file)
                if content:
                    await self.speaker.speak(f"Here's the content of {potential_file}")
                    print(f"\n{'='*50}\n{content[:500]}...\n{'='*50}")
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
                
            analysis = screen_data['analysis']
            print(f"\n{'='*50}")
            print(f"SCREEN CAPTURE: {analysis['content_type'].upper()}")
            print(f"Words: {analysis['word_count']}, Lines: {analysis['line_count']}")
            print(f"Screenshot saved to: {screen_data['screenshot_path']}")
            print(f"{'='*50}")
            
            content_type = analysis['content_type']
            word_count = analysis['word_count']
            
            summary = f"I've captured your screen. I can see {content_type} content with approximately {word_count} words."
            await self.speaker.speak(summary)
            
            if self.brain.provider in ["openai", "anthropic"]:
                await self.speaker.speak("Analyzing the content for you.")
                description = self.screen_reader.describe_for_ai(screen_data)
                ai_analysis = await self.brain.analyze_screen(description)
                print(f"\n[AI ANALYSIS]\n{ai_analysis}\n")
                await self.speaker.speak(ai_analysis[:300])
                
            return True
            
        return False
        
    async def run(self):
        """Main loop - TEXT ONLY"""
        await self.startup()
        self.running = True
        
        print("\n" + "="*50)
        print("JARVIS IS READY (TEXT MODE)")
        print("="*50)
        print("Type your commands below:")
        print("  hello        - Greeting")
        print("  what time    - Current time")
        print("  open notepad - Open applications")
        print("  read file    - Read documents")
        print("  list files   - Show files")
        print("  search xyz   - Web search")
        print("  exit         - Quit")
        print("="*50)
        print()
        
        while self.running:
            try:
                user_input = input("You: ")
                
                if user_input.lower() in ['exit', 'quit', 'goodbye', 'bye']:
                    await self.speaker.speak("Goodbye. JARVIS standing by.")
                    self.running = False
                    break
                    
                if user_input.strip():
                    await self.process_command(user_input)
                    
            except Exception as e:
                print(f"Error: {e}")


async def main():
    jarvis = JarvisText()
    await jarvis.run()


if __name__ == "__main__":
    asyncio.run(main())
