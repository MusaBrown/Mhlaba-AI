# 🤖 MHLABA - My Helpful Learning Assistant & Brilliant Aid

Your personal AI assistant with **Ollama backend** and modern web interface.

## 🏗️ Architecture

```
┌─────────────────┐      HTTP API      ┌─────────────────┐
│  mhlaba-web     │  ◄──────────────►  │  mhlaba-api     │
│  (Frontend)     │                    │  (Backend)      │
│  Netlify        │                    │  Render/VPS     │
│  React          │                    │  Ollama         │
└─────────────────┘                    └─────────────────┘
```

**No API keys needed!** You host your own Ollama backend.

## 📁 Project Structure

```
.
├── mhlaba/              # Desktop Python application
│   ├── main.py
│   ├── config.py
│   └── requirements.txt
│
├── mhlaba-api/          # Backend API (NEW!)
│   ├── src/index.js     # Express API server
│   ├── Dockerfile       # Docker config
│   ├── docker-compose.yml
│   └── README.md
│
├── mhlaba-web/          # Frontend React app
│   ├── src/App.jsx      # Chat interface
│   ├── src/config.js    # API URL config
│   └── README.md
│
├── DEPLOY_OLLAMA.md     # Full deployment guide
└── README.md            # This file
```

## 🚀 Quick Deploy

### Step 1: Deploy Backend (Ollama API)

**Option A: Docker VPS (Recommended)**

```bash
# On your VPS
git clone https://github.com/MusaBrown/Mhlaba-AI.git
cd Mhlaba-AI/mhlaba-api
docker-compose up -d

# Pull a model
docker exec mhlaba-ollama ollama pull llama3.2
```

**Option B: Render.com**
- See `DEPLOY_OLLAMA.md` for details

### Step 2: Update Frontend Config

Edit `mhlaba-web/src/config.js`:

```javascript
export const API_URL = 'https://your-api-url.com';
```

### Step 3: Deploy Frontend

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/MusaBrown/Mhlaba-AI)

Or manually:
```bash
cd mhlaba-web
npm install
npm run build
# Upload dist/ to Netlify
```

---

## 💻 Desktop Application

Voice-activated AI assistant for Windows:

```bash
cd mhlaba
pip install -r requirements.txt
python main.py
```

---

## 📚 Documentation

- **[DEPLOY_OLLAMA.md](DEPLOY_OLLAMA.md)** - Complete deployment guide
- **[mhlaba-api/README.md](mhlaba-api/README.md)** - Backend API docs
- **[mhlaba-web/README.md](mhlaba-web/README.md)** - Frontend docs

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | React + Vite |
| **Backend** | Node.js + Express |
| **AI Engine** | Ollama |
| **Models** | Llama 3.2, Llama 3.1, Mistral, etc. |
| **Hosting** | Netlify (frontend) + Render/VPS (backend) |

---

## 💰 Costs

| Service | Cost |
|---------|------|
| Netlify (Frontend) | **Free** |
| VPS (Backend) | **$6-25/month** |
| **Total** | **$6-25/month** |

Much cheaper than OpenAI API for heavy usage!

---

## 🔒 Privacy

- ✅ **Your server** - You control everything
- ✅ **No API keys** - No third-party billing
- ✅ **Private data** - Stays on your infrastructure

---

Built with ❤️ using React + Node.js + Ollama
