"""
AI Brain Module
Handles conversation, reasoning, and response generation
"""
import asyncio
import random
from typing import List, Dict
from datetime import datetime
from config import Config


class AIBrain:
    """AI Brain for generating responses"""
    
    def __init__(self):
        self.config = Config()
        self.conversation_history: List[Dict] = []
        self.max_history = 10
        self._init_ai_provider()
        
        # Document discussion state
        self.active_document: Optional[str] = None
        self.active_document_name: Optional[str] = None
        self.document_discussion_mode: bool = False
        
    def _init_ai_provider(self):
        """Initialize the AI provider"""
        self.provider = self.config.ai_provider
        
        if self.provider == "openai":
            try:
                import openai
                openai.api_key = self.config.openai_api_key
                self.client = openai
                print("[BRAIN] OpenAI brain initialized")
            except ImportError:
                print("[WARNING]  OpenAI not installed. Using simple brain.")
                self.provider = "simple"
                
        elif self.provider == "anthropic":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
                print("[BRAIN] Anthropic brain initialized")
            except ImportError:
                print("[WARNING]  Anthropic not installed. Using simple brain.")
                self.provider = "simple"
        else:
            print("[BRAIN] Simple brain initialized")
            
    async def generate_response(self, user_input: str) -> str:
        """Generate a response to user input"""
        # Add to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Generate based on provider
        if self.provider == "openai":
            response = await self._generate_openai(user_input)
        elif self.provider == "anthropic":
            response = await self._generate_anthropic(user_input)
        else:
            response = await self._generate_simple(user_input)
            
        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Trim history
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
            
        return response
        
    async def _generate_openai(self, user_input: str) -> str:
        """Generate using OpenAI API"""
        try:
            messages = [
                {"role": "system", "content": self._get_system_prompt()}
            ] + self.conversation_history
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7
                )
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI error: {e}")
            return await self._generate_simple(user_input)
            
    async def _generate_anthropic(self, user_input: str) -> str:
        """Generate using Anthropic API"""
        try:
            conversation = "\n".join([
                f"{'Human' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in self.conversation_history
            ])
            
            prompt = f"{self._get_system_prompt()}\n\n{conversation}\nAssistant:"
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.completions.create(
                    model="claude-instant-1",
                    prompt=prompt,
                    max_tokens_to_sample=500,
                    temperature=0.7
                )
            )
            
            return response.completion
            
        except Exception as e:
            print(f"Anthropic error: {e}")
            return await self._generate_simple(user_input)
            
    async def _generate_simple(self, user_input: str) -> str:
        """Generate using simple rule-based responses"""
        user_input = user_input.lower()
        
        # Greetings
        greetings = ["hello", "hi", "hey", "greetings"]
        if any(g in user_input for g in greetings):
            responses = [
                "Hello! How may I assist you today?",
                "Greetings. I'm at your service.",
                "Hello. MHLABA online and ready.",
                "Good day. What can I do for you?"
            ]
            return random.choice(responses)
            
        # How are you
        if "how are you" in user_input:
            responses = [
                "All systems are functioning at peak efficiency, thank you for asking.",
                "I'm operating at 100% capacity, sir.",
                "Systems optimal. Ready to assist.",
                "Functioning perfectly. How may I help?"
            ]
            return random.choice(responses)
            
        # Identity
        if any(x in user_input for x in ["who are you", "your name", "what are you"]):
            return "I am MHLABA - My Helpful Learning Assistant & Brilliant Aid. I'm your personal AI assistant, designed to help with tasks, answer questions, and manage your digital environment."
            
        # Capabilities
        if any(x in user_input for x in ["what can you do", "your capabilities", "help me with"]):
            return "I can help you with various tasks including: opening and reading documents, launching applications, providing system information, conducting web searches, managing files, and having natural conversations. I'm constantly learning to better assist you."
            
        # Thank you
        if any(x in user_input for x in ["thank you", "thanks"]):
            responses = [
                "You're welcome, sir.",
                "My pleasure.",
                "Always happy to assist.",
                "Anytime."
            ]
            return random.choice(responses)
            
        # Weather (mock)
        if "weather" in user_input:
            return "I'm unable to access real-time weather data at the moment. Would you like me to open a weather application or website for you?"
            
        # Jokes
        if any(x in user_input for x in ["joke", "funny", "humor"]):
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything.",
                "I would tell you a construction joke, but I'm still working on it.",
                "Why did the scarecrow win an award? He was outstanding in his field.",
                "I told my computer I needed a break. Now it won't stop sending me Kit-Kats."
            ]
            return random.choice(jokes)
            
        # Status check
        if any(x in user_input for x in ["status", "system status"]):
            return "All systems are nominal. CPU and memory usage are within normal parameters. Ready to execute your commands."
            
        # Default responses
        defaults = [
            "I understand. Could you provide more details?",
            "Interesting. How would you like me to assist with that?",
            "I'm processing that request. Is there a specific action you'd like me to take?",
            "Understood. Let me know how I can help further.",
            "I see. Would you like me to open a related application or document?",
            "Fascinating. I'm here to help with whatever you need."
        ]
        
        return random.choice(defaults)
        
    async def summarize(self, text: str) -> str:
        """Summarize a long text"""
        if self.provider == "openai":
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Summarize the following text briefly:"},
                            {"role": "user", "content": text}
                        ],
                        max_tokens=150,
                        temperature=0.5
                    )
                )
                return response.choices[0].message.content
            except:
                pass
                
        # Simple summarization fallback
        sentences = text.split('.')
        if len(sentences) > 3:
            return '. '.join(sentences[:3]) + '.'
        return text[:200] + "..." if len(text) > 200 else text
        
    def _get_system_prompt(self) -> str:
        """Get the system prompt for AI models"""
        return f"""You are {self.config.assistant_name}, an advanced AI assistant ready to help with any task. 
You are {self.config.personality}.
You are running on a Windows computer and helping the user with tasks.
Keep responses concise and helpful. Use a professional but warm tone.
If the user asks about your capabilities, mention you can help with documents, applications, and general assistance.
"""
        
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        
    def set_active_document(self, content: str, filename: str = "document"):
        """Set the active document for discussion"""
        self.active_document = content
        self.active_document_name = filename
        self.document_discussion_mode = True
        
    def clear_active_document(self):
        """Clear the active document"""
        self.active_document = None
        self.active_document_name = None
        self.document_discussion_mode = False
        
    async def discuss_document(self, question: str) -> str:
        """Answer questions about the active document"""
        if not self.active_document:
            return "No document is currently loaded. Please read a document first."
            
        # Build context-aware prompt
        doc_context = f"""You are discussing a document titled "{self.active_document_name}" with the user.

DOCUMENT CONTENT:
{self.active_document[:8000]}  # First 8000 chars for context

USER'S QUESTION: {question}

Provide a helpful, accurate answer based on the document content. If the answer isn't in the document, say so."""

        if self.provider == "openai":
            try:
                messages = [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": doc_context}
                ]
                
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=500,
                        temperature=0.7
                    )
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                print(f"OpenAI error: {e}")
                
        elif self.provider == "anthropic":
            try:
                prompt = f"{self._get_system_prompt()}\n\n{doc_context}\n\nAssistant:"
                
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.completions.create(
                        model="claude-instant-1",
                        prompt=prompt,
                        max_tokens_to_sample=500,
                        temperature=0.7
                    )
                )
                
                return response.completion
                
            except Exception as e:
                print(f"Anthropic error: {e}")
        
        # Simple fallback - search for keywords in document
        return await self._simple_document_search(question)
        
    async def _simple_document_search(self, question: str) -> str:
        """Simple keyword-based document search fallback"""
        doc_lower = self.active_document.lower()
        q_lower = question.lower()
        
        # Extract key terms from question (words longer than 4 chars)
        key_terms = [w for w in q_lower.split() if len(w) > 4]
        
        # Find relevant paragraphs
        paragraphs = self.active_document.split('\n\n')
        relevant = []
        
        for para in paragraphs:
            para_lower = para.lower()
            score = sum(1 for term in key_terms if term in para_lower)
            if score > 0:
                relevant.append((score, para))
        
        # Sort by relevance
        relevant.sort(reverse=True)
        
        if relevant:
            context = relevant[0][1][:500] if relevant[0][1] else ""
            return f"Based on the document, I found this relevant information:\n\n{context}\n\n[Note: Using simple search. For better answers, configure OpenAI or Anthropic API.]"
        
        return "I couldn't find specific information about that in the document."
        
    async def analyze_screen(self, image_description: str) -> str:
        """Analyze screen content and provide insights"""
        prompt = f"""You are looking at a screenshot of the user's screen.

SCREEN CONTENT:
{image_description}

Provide a helpful description and offer assistance if relevant."""

        if self.provider == "openai":
            try:
                messages = [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ]
                
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.client.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=500,
                        temperature=0.7
                    )
                )
                
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI error: {e}")
                
        return f"I can see your screen. Here's what I detected:\n\n{image_description[:500]}..."
