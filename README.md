# 🤖 MHLABA - My Helpful Learning Assistant & Brilliant Aid

Your personal AI assistant - available as both a desktop voice assistant and a modern web interface.

## 🌟 Features

### Desktop Application (Python)
- 🎤 **Voice Recognition** - Hands-free voice commands
- 🔊 **Text-to-Speech** - MHLABA speaks back to you
- 🧠 **AI Brain** - Conversational AI with OpenAI/Anthropic support
- 📄 **Document Reader** - Read and discuss various file formats
- 🖥️ **Screen Reader** - Analyze screen content
- ⚡ **System Commands** - Open apps, search web, get system info

### Web Interface (React)
- 💻 **Modern Chat Interface** - KimiCode-like dark theme
- 🤖 **Multiple AI Providers** - OpenAI GPT-3.5/4, Anthropic Claude
- 💾 **Persistent Conversations** - Saved in browser storage
- 📱 **Responsive Design** - Works on all devices
- 🔒 **Privacy First** - API keys stored locally only

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
└── mhlaba-web/          # Web interface
    ├── src/             # React source code
    ├── public/          # Static assets
    ├── package.json     # Node dependencies
    ├── netlify.toml     # Netlify config
    └── README.md        # Web app docs
```

## 🚀 Quick Start

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

4. **Optional: Add AI API keys** in `config.py` for smarter responses

### Web Interface

1. **Navigate to web directory**:
```bash
cd mhlaba-web
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm run dev
```

4. **Open** http://localhost:3000

## 🌐 Deploy to Netlify

### One-Click Deploy (Recommended)

Click this button to deploy directly to Netlify:

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/yourusername/mhlaba)

*(Note: You'll need to upload this to a Git repository first)*

### Manual Deploy

1. **Build the web app**:
```bash
cd mhlaba-web
npm install
npm run build
```

2. **Go to** https://app.netlify.com/drop

3. **Drag and drop** the `mhlaba-web/dist` folder

### Deploy via Git (CI/CD)

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/mhlaba.git
git push -u origin main
```

2. **Connect to Netlify**:
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Select your GitHub repository
   - Build settings are auto-configured via `netlify.toml`
   - Click "Deploy site"

## ⚙️ Configuration

### Desktop App

Edit `mhlaba/config.py`:

```python
# Change wake word
self.wake_word = "mhlaba"

# Add AI API keys
self.openai_api_key = "your-key-here"
self.anthropic_api_key = "your-key-here"
```

### Web App

1. **First time setup**: Click the Settings (⚙️) button
2. **Select AI Provider**: OpenAI or Anthropic
3. **Enter API Key**: Your key is stored only in your browser
4. **Choose Model**: GPT-3.5, GPT-4, Claude, etc.

**Get API Keys:**
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/settings/keys

## 🎨 Customization

### Change the Name

To rename from "MHLABA" to something else:

1. **Desktop**: Edit `mhlaba/config.py`
   ```python
   self.assistant_name = "YOUR_NAME"
   self.wake_word = "your_wake_word"
   ```

2. **Web**: Edit `mhlaba-web/src/App.jsx` and `mhlaba-web/index.html`

### Customize Theme

Edit `mhlaba-web/src/App.css`:

```css
:root {
  --bg-primary: #0d0d0d;      /* Background */
  --accent-primary: #6366f1;   /* Primary color */
  --accent-secondary: #a855f7; /* Secondary color */
}
```

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

### Desktop App

**Microphone not working:**
- Check microphone is connected and set as default
- Adjust `energy_threshold` in `config.py`

**Voice not speaking:**
- Check speakers/headphones are connected
- Try running as administrator

**Import errors:**
```bash
pip install -r requirements.txt
```

### Web App

**"Please set your API key" error:**
- Click Settings and enter your API key
- Ensure you're using the correct provider

**Build fails:**
- Use Node.js 18+: `nvm use 18`
- Delete `node_modules` and reinstall

## 📄 License

Personal use only. Have fun with your own MHLABA!

---

Built with ❤️ using Python + React
