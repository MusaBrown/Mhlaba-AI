# MHLABA Web Interface

A modern, KimiCode-like web interface for MHLABA AI Assistant - **runs entirely in your browser with NO API keys needed!**

## 🌟 Features

- 🎨 **Modern Dark Theme** - Clean, professional interface inspired by KimiCode
- 💬 **Real-time Chat** - Smooth messaging experience with markdown support
- 🤖 **Browser-Based AI** - Uses WebLLM to run models directly in your browser
- 🆓 **100% Free** - No API keys, no subscriptions, no server costs
- 🔒 **Privacy First** - All processing happens locally on your device
- 💾 **Local Storage** - Conversations saved locally in your browser
- 📱 **Responsive Design** - Works on desktop and mobile devices

## 🚀 How It Works

MHLABA uses [WebLLM](https://github.com/mlc-ai/web-llm) to download and run AI models directly in your browser using WebGPU:

1. **First Visit**: Download an AI model (1-5 GB, one-time download)
2. **Chat**: The model runs entirely on your device - no data sent to servers
3. **Persist**: Model stays cached, conversations saved locally

## 🛠️ System Requirements

- **Browser**: Chrome 113+ or Edge 113+ (WebGPU required)
- **RAM**: 8GB+ recommended (models are 1-5 GB)
- **Storage**: 10GB free space for model caching

### Enable WebGPU

WebGPU is enabled by default in Chrome/Edge 113+. If not:

1. Go to `chrome://flags/#enable-unsafe-webgpu`
2. Set to "Enabled"
3. Restart browser

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Navigate to the web directory:
```bash
cd mhlaba-web
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open http://localhost:3000 in your browser

### Building for Production

```bash
npm run build
```

The build output will be in the `dist` directory.

## 🌐 Deploy to Netlify

### One-Click Deploy (Recommended)

Click this button to deploy directly to Netlify:

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

### Deploy via Git (Auto-Deploy)

1. Push your code to GitHub (already done!)
2. Connect to Netlify:
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Choose `MusaBrown/Mhlaba-AI`
   - Build settings will be auto-detected
   - Click "Deploy site"

## 🧠 Available Models

Choose from several models depending on your needs:

| Model | Size | Best For |
|-------|------|----------|
| **Gemma 2 2B** | 1.6 GB | Fastest, lowest resource usage |
| **Phi-3 Mini** | 1.8 GB | Quick responses, efficient |
| **Llama 3.1 8B** | 4.5 GB | Best overall quality |
| **Qwen 2.5 7B** | 4.3 GB | Multilingual support |
| **Mistral 7B** | 4.5 GB | High quality responses |

## 📁 Project Structure

```
mhlaba-web/
├── public/
│   └── favicon.svg
├── src/
│   ├── App.jsx       # Main application component (WebLLM integration)
│   ├── App.css       # Styles with KimiCode-like theme
│   └── main.jsx      # Entry point
├── index.html        # HTML template
├── package.json      # Dependencies
├── vite.config.js    # Vite configuration
├── netlify.toml      # Netlify deployment config
└── README.md         # This file
```

## 🎨 Customization

### Changing the Theme

Edit `src/App.css` to customize colors:

```css
:root {
  --bg-primary: #0d0d0d;      /* Main background */
  --bg-secondary: #1a1a1a;    /* Sidebar background */
  --accent-primary: #6366f1;   /* Primary accent color */
  --accent-secondary: #a855f7; /* Secondary accent color */
  /* ... more variables */
}
```

### Adding Models

To add more models, edit the `AVAILABLE_MODELS` array in `src/App.jsx`:

```javascript
const AVAILABLE_MODELS = [
  {
    id: "Model-Name-q4f32_1-MLC",
    name: "Display Name",
    description: "Description",
    size: "X GB",
    quant: "q4f32"
  },
  // ...
]
```

Find available models at: https://github.com/mlc-ai/web-llm/blob/main/src/config.ts

## ⌨️ Keyboard Shortcuts

- `Enter` - Send message
- `Shift + Enter` - New line in message
- `Esc` - Close modals

## 🐛 Troubleshooting

### "WebGPU not supported" error
- Update Chrome/Edge to version 113+
- Enable WebGPU flag: `chrome://flags/#enable-unsafe-webgpu`
- Try a different browser

### Model download fails
- Check you have enough disk space (10GB+)
- Ensure stable internet connection
- Try a smaller model first (Gemma 2 2B)

### Slow responses
- Use a smaller model (Gemma 2 2B or Phi-3 Mini)
- Close other browser tabs
- Ensure your device has enough free RAM

### Out of memory errors
- Use Gemma 2 2B (smallest model)
- Close other applications
- Consider upgrading RAM

### Build fails
- Use Node.js 18+: `nvm use 18`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

## 🔒 Privacy & Security

- **No data leaves your device** - Everything runs locally
- **No API keys** - No accounts or authentication needed
- **Conversations stored locally** - In browser's localStorage
- **Models cached locally** - Downloaded once, reused across sessions

## 📝 Notes

- First load takes time (downloading the AI model)
- Models are cached by the browser
- Requires modern browser with WebGPU support
- Performance depends on your device's capabilities

## 📄 License

Personal use only.

---

Built with ❤️ using React + WebLLM + Vite
