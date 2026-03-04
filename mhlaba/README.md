# 🤖 MHLABA - My Helpful Learning Assistant & Brilliant Aid

A voice-activated AI assistant for Windows inspired by advanced AI systems. Can open documents, answer questions, execute system commands, and hold conversations.

## Features

- 🎤 **Voice Recognition**: Listen and respond to voice commands
- 🔊 **Text-to-Speech**: MHLABA speaks back to you
- 🧠 **AI Brain**: Conversational AI with context awareness
- 📄 **Document Reader**: Read various file formats (txt, pdf, docx, etc.)
- 💭 **Document Discussion**: Read along with MHLABA and discuss documents together
- 🖥️ **Screen Reader**: MHLABA can see your screen and describe what's on it
- ⚡ **System Commands**: Open apps, get system info, search the web
- 💬 **Natural Conversation**: Chat naturally about various topics

## Installation

1. **Install Python 3.8+** from [python.org](https://python.org)

2. **Install required packages**:
```bash
pip install -r requirements.txt
```

**Note**: If you have issues with PyAudio on Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

3. **Optional: Add AI API keys** for smarter responses:
   - OpenAI: Set `OPENAI_API_KEY` environment variable
   - Anthropic: Set `ANTHROPIC_API_KEY` environment variable

   Without API keys, JARVIS uses a built-in rule-based AI.

## Usage

### Run MHLABA
```bash
cd mhlaba
python main.py
```

### Commands

#### Voice Commands
Say "Mhlaba" followed by your command:
- "Mhlaba, what time is it?"
- "Mhlaba, open Chrome"
- "Mhlaba, read my document.txt"

#### Text Commands
Type directly in the terminal:
- `hello` - Greeting
- `what can you do` - List capabilities
- `open notepad` - Open applications
- `read filename.txt` - Read documents
- `system info` - Show computer stats
- `list files` - Show files in current directory
- `search for python tutorials` - Web search
- `exit` - Quit JARVIS

#### Document Discussion Commands
After reading a document, MHLABA enters discussion mode:
- Ask questions about the document: *"What does it say about the main topic?"*
- Get clarifications: *"Explain this section"*
- Find specific info: *"What are the key points?"*
- Exit discussion: *"Stop discussing"* or *"Close document"*

#### Screen Reading Commands
- *"Read my screen"* or *"What's on my screen"* - Capture and describe screen content
- *"Describe what you see"* - Get AI analysis of screen content
- Works with documents, web pages, code, and more

## Project Structure

```
mhlaba/
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

Edit `config.py` to customize:
- Wake word (default: "mhlaba")
- Voice settings
- AI provider
- Personality traits

## Windows Compatibility

This project is designed specifically for Windows and uses Windows-specific features like:
- `os.startfile()` for opening files
- Windows speech synthesis voices
- Windows path handling

## Troubleshooting

### Microphone not working
- Check your microphone is connected and set as default
- Adjust `energy_threshold` in `config.py`

### Voice not speaking
- Check your speakers/headphones are connected
- Try running as administrator if needed

### Import errors
- Make sure all requirements are installed: `pip install -r requirements.txt`

### Screen reading not working
- **OCR not available**: Install Tesseract-OCR from https://github.com/UB-Mannheim/tesseract/wiki
- **Screenshot failed**: Make sure you have Pillow installed: `pip install Pillow`
- **Tesseract not found**: Add Tesseract installation directory to your PATH

### Document discussion not working
- For best results, configure OpenAI or Anthropic API keys in `config.py`
- Without API keys, JARVIS uses simple keyword search (limited functionality)

## License

Personal use only. Have fun with your own MHLABA!
