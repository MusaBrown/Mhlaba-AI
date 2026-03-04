# 🤖 JARVIS - Just A Rather Very Intelligent System

A voice-activated AI assistant for Windows inspired by Iron Man's JARVIS.

## Features

- 🎤 **Voice Recognition** - Listen and respond to voice commands
- 🔊 **Text-to-Speech** - JARVIS speaks back to you
- 🧠 **AI Brain** - Conversational AI with OpenAI/Anthropic support
- 📄 **Document Reader** - Read various file formats (txt, pdf, docx, etc.)
- 💭 **Document Discussion** - Read along with JARVIS and discuss documents together
- 🖥️ **Screen Reader** - JARVIS can see your screen and describe what's on it
- ⚡ **System Commands** - Open apps, get system info, search the web
- 💬 **Natural Conversation** - Chat naturally about various topics

## Quick Start

1. **Install Python 3.8+** from [python.org](https://python.org)

2. **Install dependencies**:
```bash
cd jarvis
pip install -r requirements.txt
```

3. **Run JARVIS**:
```bash
python main.py
```

## Optional: Add AI API Keys

For smarter responses, add API keys in `jarvis/config.py`:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys

Without API keys, JARVIS uses a built-in rule-based AI.

## Voice Commands

Say "Jarvis" followed by your command:
- "Jarvis, what time is it?"
- "Jarvis, open Chrome"
- "Jarvis, read my document.txt"

## Project Structure

```
jarvis/
├── main.py              # Main entry point
├── config.py            # Configuration settings
├── voice_listener.py    # Speech recognition
├── voice_speaker.py     # Text-to-speech
├── ai_brain.py          # AI response generation
├── document_handler.py  # File reading
├── screen_reader.py     # Screen capture and OCR
├── system_executor.py   # System commands
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Customization

Edit `jarvis/config.py` to customize:
- Wake word (default: "jarvis")
- Voice settings
- AI provider
- Personality traits

## License

Personal use only. Have fun with your own JARVIS!
