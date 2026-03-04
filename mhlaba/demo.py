#!/usr/bin/env python3
"""
JARVIS Interactive Demo
Text-based demonstration of JARVIS capabilities
"""

import asyncio
from ai_brain import AIBrain
from document_handler import DocumentHandler
from system_executor import SystemExecutor


class JarvisDemo:
    def __init__(self):
        print("="*60)
        print("       JARVIS - Interactive Demo")
        print("="*60)
        print()
        
        self.brain = AIBrain()
        self.docs = DocumentHandler()
        self.executor = SystemExecutor()
        
    async def run(self):
        print("[JARVIS] JARVIS online. Systems operational.")
        print("[JARVIS] How may I assist you today?")
        print()
        print("Available commands:")
        print("  - Conversation: hello, how are you, who are you")
        print("  - System: time, date, system info, list files")
        print("  - Files: read <filename>, show files")
        print("  - Quit: exit, bye, quit")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print("[JARVIS] Goodbye, sir. JARVIS standing by.")
                    break
                    
                await self.process_command(user_input)
                print()
                
            except KeyboardInterrupt:
                print("\n[JARVIS] Goodbye!")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                
    async def process_command(self, command: str):
        command_lower = command.lower()
        
        # Time
        if "time" in command_lower:
            from datetime import datetime
            current_time = datetime.now().strftime("%I:%M %p")
            print(f"[JARVIS] The current time is {current_time}")
            return
            
        # Date
        if "date" in command_lower or "day" in command_lower:
            from datetime import datetime
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            print(f"[JARVIS] Today is {current_date}")
            return
            
        # System info
        if "system info" in command_lower or "computer info" in command_lower:
            info = self.executor.get_system_info()
            print(f"[JARVIS] {info}")
            return
            
        # List files
        if "list files" in command_lower or "show files" in command_lower:
            files = self.docs.list_files()
            if files:
                file_list = ", ".join(files[:10])
                response = f"Files in current directory: {file_list}"
                if len(files) > 10:
                    response += f" and {len(files) - 10} more"
            else:
                response = "No files found in the current directory"
            print(f"[JARVIS] {response}")
            return
            
        # Read file
        if "read" in command_lower:
            words = command_lower.split()
            for i, word in enumerate(words):
                if word == "read" and i + 1 < len(words):
                    filename = " ".join(words[i+1:])
                    content = self.docs.read_document(filename)
                    if content:
                        print(f"[JARVIS] Content of {filename}:")
                        print("-" * 40)
                        preview = content[:500] + "..." if len(content) > 500 else content
                        print(preview)
                        print("-" * 40)
                    else:
                        print(f"[JARVIS] Could not find or read file: {filename}")
                    return
                    
        # Default: AI conversation
        response = await self.brain.generate_response(command)
        print(f"[JARVIS] {response}")


async def main():
    demo = JarvisDemo()
    await demo.run()


if __name__ == "__main__":
    asyncio.run(main())
