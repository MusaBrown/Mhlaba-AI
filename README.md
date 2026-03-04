# 🤖 MHLABA - My Helpful Learning Assistant & Brilliant Aid

Your personal AI assistant - available as both a desktop voice assistant and a **browser-based web interface with NO API keys needed!**

## 🌟 Features

### Desktop Application (Python)
- 🎤 **Voice Recognition** - Hands-free voice commands
- 🔊 **Text-to-Speech** - MHLABA speaks back to you
- 🧠 **AI Brain** - Conversational AI with OpenAI/Anthropic support
- 📄 **Document Reader** - Read and discuss various file formats
- 🖥️ **Screen Reader** - Analyze screen content
- ⚡ **System Commands** - Open apps, search web, get system info

### Web Interface (React + WebLLM) 🆕
- 💻 **Modern Chat Interface** - KimiCode-like dark theme
- 🤖 **Browser-Based AI** - Runs locally using WebLLM
- 🆓 **100% Free** - No API keys, no subscriptions!
- 🔒 **Privacy First** - All processing on your device
- 💾 **Persistent Conversations** - Saved in browser storage
- 📱 **Responsive Design** - Works on all devices

## 📁 Project Structure

```
.
├── mhlaba/              # Desktop Python application
│   ├── main.py          # Main entry point
│   ├── config.py        # Configuration
│   ├── ai_brain.py      # AI logic
│   ├── requirements.txt # Python dependencies
│   └── README.md        # Desktop app docs
│
└── mhlaba-web/          # Web interface (React + WebLLM)
    ├── src/             # React source code
    ├── public/          # Static assets
    ├── package.json     # Node dependencies
    ├── netlify.toml     # Netlify config
    └── README.md        # Web app docs
```

## 🚀 Quick Start

### Web Interface (Recommended - No Setup!)

**Live Demo**: https://mhlaba-ai.netlify.app

Or run locally:
```bash
cd mhlaba-web
npm install
npm run dev
```

**How it works:**
1. Visit the site
2. Click "Load AI Model" 
3. Choose a model (Gemma 2 2B is fastest)
4. Wait for download (1-5 GB, one-time)
5. Start chatting!

### Desktop Application

1. **Install Python 3.8+** from [python.org](https://python.org)

2. **Install dependencies**:
```bash
cd mhlaba
pip install -r requirements.txt
```

3. **Run MHLABA**:
```bash
python main.py
```

4. **Optional: Add AI API keys** in `config.py` for cloud AI

## 🌐 Deploy to Netlify (Web Interface)

### One-Click Deploy

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/MusaBrown/Mhlaba-AI)

### Manual Deploy

1. **Build the web app**:
```bash
cd mhlaba-web
npm install
npm run build
```

2. **Go to** https://app.netlify.com/drop

3. **Drag and drop** the `mhlaba-web/dist` folder

## 🧠 Available AI Models (Web)

Choose based on your device's capabilities:

| Model | Size | RAM Needed | Speed | Quality |
|-------|------|------------|-------|---------|
| **Gemma 2 2B** ⭐ | 1.6 GB | 4GB | ⚡⚡⚡ | ⭐⭐⭐ |
| **Phi-3 Mini** | 1.8 GB | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| **Llama 3.1 8B** | 4.5 GB | 8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| **Mistral 7B** | 4.5 GB | 8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| **Qwen 2.5 7B** | 4.3 GB | 8GB | ⚡⚡ | ⭐⭐⭐⭐ |

## ⚙️ Configuration

### Desktop App

Edit `mhlaba/config.py`:

```python
# Change wake word
self.wake_word = "mhlaba"

# Add AI API keys (optional - for cloud AI)
self.openai_api_key = "your-key-here"
self.anthropic_api_key = "your-key-here"
```

### Web App

**No configuration needed!** Just:
1. Visit the site
2. Load a model
3. Start chatting

## 📝 Available Commands (Desktop)

### Voice Commands
Say "Mhlaba" followed by:
- "What time is it?" - Get current time
- "Open Chrome" - Open applications
- "Read my document.txt" - Read files
- "What's on my screen?" - Screen analysis
- "Search for Python tutorials" - Web search

### Text Commands
Type directly in the terminal:
- `hello` - Greeting
- `what can you do` - List capabilities
- `open notepad` - Open applications
- `system info` - Computer stats
- `exit` - Quit MHLABA

## 🛠️ Troubleshooting

### Web App

**"WebGPU not supported" error:**
- Use Chrome 113+ or Edge 113+
- Enable WebGPU: `chrome://flags/#enable-unsafe-webgpu`

**Model download fails:**
- Check disk space (need 10GB free)
- Ensure stable internet
- Try a smaller model (Gemma 2 2B)

**Slow responses:**
- Use Gemma 2 2B or Phi-3 Mini
- Close other browser tabs

### Desktop App

**Microphone not working:**
- Check microphone is connected and set as default
- Adjust `energy_threshold` in `config.py`

**Voice not speaking:**
- Check speakers/headphones are connected
- Try running as administrator

## 🔒 Privacy

### Web App
- ✅ **No data leaves your device**
- ✅ **No API keys needed**
- ✅ **No accounts or sign-ups**
- ✅ **All processing is local**

### Desktop App
- ✅ Local voice processing
- ✅ Optional cloud AI (only if you add API keys)

## 🎨 Customization

### Change the Name

1. **Web**: Edit `mhlaba-web/src/App.jsx` and `index.html`
2. **Desktop**: Edit `mhlaba/config.py`

### Customize Theme

Edit `mhlaba-web/src/App.css`:

```css
:root {
  --bg-primary: #0d0d0d;
  --accent-primary: #6366f1;
  --accent-secondary: #a855f7;
}
```

## 📄 License

Personal use only. Have fun with your own MHLABA!

---

Built with ❤️ using Python + React + WebLLM
