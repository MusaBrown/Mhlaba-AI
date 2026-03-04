# MHLABA Web Interface

A modern, KimiCode-like web interface for MHLABA AI Assistant.

## 🌟 Features

- 🎨 **Modern Dark Theme** - Clean, professional interface inspired by KimiCode
- 💬 **Real-time Chat** - Smooth messaging experience with markdown support
- 🔗 **Ollama API Integration** - Connects to your Ollama backend
- 💾 **Local Storage** - Conversations saved in browser
- 📱 **Responsive Design** - Works on desktop and mobile devices

## 🏗️ Architecture

This frontend connects to a separate **MHLABA API** backend that runs Ollama:

```
┌─────────────────┐      HTTP API      ┌─────────────────┐
│  mhlaba-web     │  ◄──────────────►  │  mhlaba-api     │
│  (This repo)    │    (You deploy)    │  (Ollama)       │
│  Netlify        │                    │  Render/Docker  │
└─────────────────┘                    └─────────────────┘
```

## 🚀 Quick Start

### 1. Deploy the Backend First

See `../mhlaba-api/README.md` for backend deployment instructions.

### 2. Update API URL

Edit `src/config.js`:

```javascript
export const API_URL = 'https://your-api-url.onrender.com';
```

### 3. Run Locally

```bash
cd mhlaba-web
npm install
npm run dev
```

4. Open http://localhost:3000

## 🌐 Deploy to Netlify

### Prerequisites

- Backend API must be deployed first
- Update `src/config.js` with your API URL

### Deploy

```bash
cd mhlaba-web
npm install
npm run build
```

Then drag `dist` folder to https://app.netlify.com/drop

Or connect GitHub repo for auto-deploy.

## ⚙️ Configuration

Edit `src/config.js`:

```javascript
// Your deployed API URL
export const API_URL = 'https://mhlaba-api.onrender.com';

// Default model (must match what's installed on Ollama)
export const DEFAULT_MODEL = 'llama3.2';
```

## 📁 Project Structure

```
mhlaba-web/
├── src/
│   ├── App.jsx       # Main chat interface
│   ├── App.css       # KimiCode-like theme
│   ├── config.js     # API configuration
│   └── main.jsx      # Entry point
├── index.html
├── package.json
├── netlify.toml
└── README.md
```

## 📝 Environment Variables (Optional)

Create `.env.local`:

```
REACT_APP_API_URL=https://your-api-url.onrender.com
```

## 🐛 Troubleshooting

### "Cannot connect to API server"
- Check that your backend is running
- Verify `API_URL` in `config.js` is correct
- Check browser console for CORS errors

### CORS errors
- Update CORS settings in `mhlaba-api/src/index.js`
- Add your Netlify domain to `corsOptions.origin`

## 📄 License

Personal use only.
