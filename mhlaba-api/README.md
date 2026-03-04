# MHLABA API

Ollama backend API for MHLABA AI Assistant.

## Overview

This is a lightweight API server that:
- Connects to an Ollama instance
- Handles CORS for the web frontend
- Provides a clean REST API for chat/completions

## Deployment Options

### Option 1: Render.com (Recommended)

1. Create account at https://render.com
2. Create a new **Web Service**
3. Connect this GitHub repo
4. Settings:
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Environment**: Node
5. Add environment variable:
   - `OLLAMA_HOST`: Your Ollama server URL
6. Deploy!

### Option 2: Self-Hosted with Ollama

1. Install Ollama: https://ollama.com/download
2. Pull a model: `ollama pull llama3.2`
3. Run Ollama: `ollama serve`
4. Set `OLLAMA_HOST=http://localhost:11434`
5. Run this API: `npm install && npm start`

### Option 3: Docker Compose (Ollama + API together)

See `docker-compose.yml`

## API Endpoints

### Health Check
```
GET /api/health
```

### List Models
```
GET /api/models
```

### Chat (Conversational)
```
POST /api/chat
Content-Type: application/json

{
  "model": "llama3.2",
  "messages": [
    { "role": "system", "content": "You are MHLABA..." },
    { "role": "user", "content": "Hello!" }
  ],
  "stream": false
}
```

### Generate (Simple)
```
POST /api/generate
Content-Type: application/json

{
  "model": "llama3.2",
  "prompt": "What is AI?",
  "stream": false
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `DEFAULT_MODEL` | `llama3.2` | Default model to use |
| `PORT` | `3001` | API server port |

## Connecting Frontend

After deploying, update your frontend's `API_URL`:

```javascript
// mhlaba-web/src/config.js
const API_URL = 'https://your-render-app.onrender.com';
```

## CORS Configuration

Update `corsOptions.origin` in `src/index.js` with your frontend URL:

```javascript
const corsOptions = {
  origin: [
    'https://mhlaba-ai-xxx.netlify.app',  // Your Netlify site
  ],
  // ...
};
```
