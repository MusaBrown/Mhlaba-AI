"""
JARVIS Configuration
"""
import os
from pathlib import Path


class Config:
    """Configuration settings for JARVIS"""
    
    def __init__(self):
        # Voice settings
        self.use_wake_word = True
        self.wake_word = "jarvis"
        self.voice_id = None  # None for default voice
        self.speech_rate = 175  # Words per minute
        
        # AI Model settings
        self.use_local_model = False  # Set to True to use local LLM
        self.local_model_path = None
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        # Default to a simple rule-based AI if no API keys
        self.ai_provider = "simple"  # Options: "simple", "openai", "anthropic"
        
        if self.openai_api_key:
            self.ai_provider = "openai"
        elif self.anthropic_api_key:
            self.ai_provider = "anthropic"
            
        # Listening settings
        self.energy_threshold = 800   # Lower = more sensitive (800-1500 recommended)
        self.pause_threshold = 1.5  # Seconds of silence before processing
        self.phrase_threshold = 0.5
        
        # Paths
        self.base_dir = Path(__file__).parent
        self.documents_dir = Path.home() / "Documents"
        
        # Personality
        self.assistant_name = "JARVIS"
        self.personality = "helpful, professional, witty, and efficient like the AI from Iron Man"
        
    def get_ai_config(self):
        """Get AI-specific configuration"""
        return {
            "provider": self.ai_provider,
            "model": "gpt-3.5-turbo" if self.ai_provider == "openai" else "claude-instant-1",
            "temperature": 0.7,
            "max_tokens": 500
        }
